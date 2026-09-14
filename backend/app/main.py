from fastapi import FastAPI
from .routers import r_application, r_deployment
app = FastAPI()
app.include_router(r_application.router)
app.include_router(r_deployment.router)


@app.get("/health")
def health():
    return {"status": "ok"}


