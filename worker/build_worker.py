import redis
import os
import time
import shutil
from backend.app.database import SessionLocal
from backend.app.models import deployment
from backend.app.models.deployment import Deployment
from backend.app.models.application import Application
from pathlib import Path 
from backend.app.services.docker import authenticate
from backend.app.services.build import build_application

host = os.getenv("REDIS_HOST", "redis")

redis_client = redis.Redis(
    host=host,
    port=6379,
    decode_responses=True,
    socket_timeout=None
)
authenticate()

def dead_letter_queue(data,error):
    data["error"]=error
    redis_client.xadd("dead_letter_jobs",data)


def retry_job(data):
    time.sleep(10)
    redis_client.xadd("build_jobs",data)

def process_job(data, message_id):
    attempts = int(data.get("attempts", 0)) + 1
    deployment_id = int(data["deployment_id"])
    application_id = int(data["application_id"])

    build_directory = Path(f"/tmp/builds/{deployment_id}/{application_id}")
    db = SessionLocal()

    try:
        deployment = (db.query(Deployment).filter(Deployment.id == deployment_id).first())

        if not deployment:
            print(f"Deployment {deployment_id} not found", flush=True)
            return

        resolved_sha, image = build_application(
            repository_url=data["repository_url"],
            commit_sha=data["commit_sha"],
            build_directory=build_directory,
            application_id=application_id,
            registry_username=os.environ["DOCKER_USERNAME"]
        )

        deployment.status = "success"
        db.commit()
        print(f"Build successful: {image}", flush=True)

    except Exception as e:
        db.rollback()
        print(f"Build attempt {attempts} failed: {e}", flush=True)

        if attempts < 3:
            data["attempts"] = str(attempts)
            retry_job(data)
            print(f"Retrying deployment {deployment_id}", flush=True)
        else:
            deployment = (db.query(Deployment).filter(Deployment.id == deployment_id).first())
            if deployment:
                deployment.status = "failed"
                db.commit()
            dead_letter_queue(data,e)
            print(f"Deployment {deployment_id} moved to dead-letter queue", flush=True)

    finally:
        db.close()
        redis_client.xack("build_jobs", "build_workers", message_id)
        shutil.rmtree(build_directory, ignore_errors=True)


while True:
    print("Waiting for jobs...", flush=True)
    try:
        jobs = redis_client.xreadgroup(
            groupname="build_workers",
            consumername="worker-1",
            streams={"build_jobs": ">"},
            count=1,
            block=5000
        )
        print(f"Redis returned: {jobs}", flush=True)
        if jobs:
            for stream, messages in jobs:
                for message_id, data in messages:
                    print(f"Processing job: {data}", flush=True)
                    process_job(data,message_id)

    except redis.exceptions.TimeoutError as e:
        print(f"Redis timeout: {e}", flush=True)
        time.sleep(1)