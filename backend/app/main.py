from fastapi import FastAPI
from .routers import r_application, r_deployment
from .redis import redis_client
app = FastAPI()
app.include_router(r_application.router)
app.include_router(r_deployment.router)


@app.get("/redis-test")
def redis_test():
    redis_client.set("forge:test", "hello")
    value = redis_client.get("forge:test")
    return {"redis": value}

@app.get("/health")
def health():
    return {"status": "ok"}


