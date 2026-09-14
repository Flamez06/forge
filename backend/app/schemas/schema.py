from pydantic import BaseModel,ConfigDict
from datetime import datetime
class ApplicationCreate(BaseModel):
    name: str
    repository_url: str
    
class ApplicationResponse(BaseModel):
    id: int
    name: str
    repository_url: str
    # if input data is an instance of the Application model instead of dict/JSON, the from_attributes=True option allows Pydantic to 
    # automatically populate the fields of the ApplicationResponse model with the corresponding attributes from the Application model.
    model_config = ConfigDict(from_attributes=True)
    
class DeploymentCreate(BaseModel):
    application_id: int
    commit_sha: str
    
class DeploymentResponse(BaseModel):
    id : int
    application_id: int
    status: str
    commit_sha: str
    created_at: datetime
    model_config = ConfigDict(from_attributes=True)
    
class DeployRequest(BaseModel):
    commit_sha: str