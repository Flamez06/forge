from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from pathlib import Path
from backend.app.services.build import build_application
from backend.app.models.application import Application
from backend.app.database import get_db
from backend.app.models.deployment import Deployment
from backend.app.schemas.schema import DeploymentResponse, DeployRequest

router = APIRouter(
    prefix="/deployments",
    tags=["deployments"]
)

# @router.post("/",response_model=DeploymentResponse)
# def create_deployment(deployment: DeploymentCreate, db: Session = Depends(get_db)):
#     application = db.query(Application).filter(Application.id == deployment.application_id).first()
#     if not application:
#         raise HTTPException(status_code=404, detail="Application not found")
#     new_deployment = Deployment(
#         application_id=deployment.application_id,
#         commit_sha=deployment.commit_sha,
#     )
#     db.add(new_deployment)
#     db.commit()
#     db.refresh(new_deployment)
#     return new_deployment

@router.get("/",response_model=list[DeploymentResponse])
def get_deployments(db: Session = Depends(get_db)):
    deployments = db.query(Deployment).all()
    return deployments

@router.post("/{application_id}/deploy",response_model=DeploymentResponse)
def create_deployment_for_application(application_id: int, data: DeployRequest, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    new_deployment = Deployment(
        application_id=application_id,
        commit_sha=data.commit_sha,
        status = "building"
    )
       
    db.add(new_deployment)
    db.commit()
    db.refresh(new_deployment)
    return new_deployment

@router.delete("/{deployment_id}", response_model=DeploymentResponse)
def delete_deployment(deployment_id: int, db: Session = Depends(get_db)):
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if deployment is None:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )
    db.delete(deployment)
    db.commit()
    return deployment

@router.get("/{deployment_id}", response_model=DeploymentResponse)
def get_deployment(deployment_id: int, db: Session = Depends(get_db)):
    deployment = db.query(Deployment).filter(Deployment.id == deployment_id).first()
    if deployment is None:
        raise HTTPException(
            status_code=404,
            detail="Deployment not found"
        )
    return deployment