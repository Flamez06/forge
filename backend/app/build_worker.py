import redis 

redis_client = redis.Redis(host='redis', port=6379, decode_responses=True)

while True:
    jobs = redis_client.xread({"build_jobs": "$"}, block=500)
    if jobs:
        print(jobs)