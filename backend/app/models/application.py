from sqlalchemy import Column, Integer, String
from ..database import Base
from sqlalchemy.orm import relationship


class Application(Base):
    __tablename__ = "applications"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    repository_url = Column(String, nullable=False) 
    # back_populates allows application.deployments to access the related Deployment objects and vice versa.
    deployments = relationship("Deployment", back_populates="application")