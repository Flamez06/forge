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
                    deployment_id = int(data.get("deployment_id"))
                    application_id = int(data.get("application_id"))
                    
                    build_directory = Path(f"/tmp/builds/{deployment_id}/{application_id}")
                    
                    db = SessionLocal()
                    try:
                        deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
                        if not deployment:
                            print(f"Deployment {deployment_id} not found", flush=True)
                            continue
                        try:
                            resolved_sha, image = build_application(
                                repository_url=data["repository_url"],
                                commit_sha=data["commit_sha"],
                                build_directory=build_directory,
                                application_id=application_id,
                                registry_username=os.environ["DOCKER_USERNAME"]
                            )
                            print(f"Build successful: {image}", flush=True)
                            deployment.status = "success"
                            db.commit()
                            redis_client.xack("build_jobs", "build_workers", message_id)
                        
                        except Exception as e:
                            db.rollback()
                            deployment.status = "failed"
                            db.commit()
                            print(f"Build failed: {e}", flush=True)
                            
                    finally:
                        db.close()
                        shutil.rmtree(build_directory, ignore_errors=True)
                        
    except redis.exceptions.TimeoutError as e:
        print(f"Redis timeout: {e}", flush=True)
        time.sleep(1)