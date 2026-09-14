from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ..database import get_db
from ..models.application import Application
from ..models.deployment import Deployment
from ..schemas.schema import DeploymentCreate, DeploymentResponse

router = APIRouter(
    prefix="/deployments",
    tags=["deployments"]
)

@router.post("/",response_model=DeploymentResponse)
def create_deployment(deployment: DeploymentCreate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == deployment.application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    new_deployment = Deployment(
        application_id=deployment.application_id,
        commit_sha=deployment.commit_sha,
    )
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    return new_deployment

@router.get("/",response_model=list[DeploymentResponse])
def get_deployments(db: Session = Depends(get_db)):
    deployments = db.query(Deployment).all()
    return deployments