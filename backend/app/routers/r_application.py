from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend.app.database import get_db
from backend.app.models.application import Application
from backend.app.schemas.schema import ApplicationCreate, ApplicationResponse, DeploymentResponse

router = APIRouter(
    prefix="/applications",
    tags=["applications"]
)

#response_model=ApplicationResponse specifies that the response of this endpoint will be an instance of the ApplicationResponse model.

@router.post("/",response_model=ApplicationResponse)
# application variable expects and validates a request body of type ApplicationCreate, which is defined in the schemas/applications.py file. 
# The get_db function is used to get a database session for the request.
def create_application(application: ApplicationCreate, db: Session = Depends(get_db)):
    new_application = Application(
        name=application.name,
        repository_url=application.repository_url
    )
    db.add(new_application)
    db.commit()
    db.refresh(new_application)
    return new_application

@router.get("/",response_model=list[ApplicationResponse])
def get_applications(db: Session = Depends(get_db)):
    applications = db.query(Application).all() # Application is the table name in sqlalchemy.
    return applications

@router.get("/{application_id}",response_model=ApplicationResponse)
def get_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    return application

@router.delete("/{application_id}",response_model=ApplicationResponse)
def delete_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    db.delete(application)
    db.commit()
    return application

@router.put("/{application_id}",response_model=ApplicationResponse)
def update_application(application_id: int, updated_application: ApplicationCreate, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    application.name = updated_application.name
    application.repository_url = updated_application.repository_url
    db.commit()
    db.refresh(application)
    return application

@router.get("/{application_id}/deployments",response_model=list[DeploymentResponse])
def get_deployments_for_application(application_id: int, db: Session = Depends(get_db)):
    application = db.query(Application).filter(Application.id == application_id).first()
    if not application:
        raise HTTPException(status_code=404, detail="Application not found")
    deployments = application.deployments
    return deployments

