import redis
import os 
host = os.getenv(
        "REDIS_HOST",
        "redis"
    )
redis_client = redis.Redis(host=host, port=6379, decode_responses=True)

while True:
    jobs = redis_client.xread({"build_jobs": "0-0"}, block=500)
    if jobs:
        print(jobs,flush=True)