import redis 

redis_client = redis.Redis(host='forge-redis', port=6379, decode_responses=True)