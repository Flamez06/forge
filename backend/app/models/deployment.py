from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from ..database import Base
from sqlalchemy.orm import relationship

class Deployment(Base):
    __tablename__ = "deployments"

    id = Column(Integer, primary_key=True)
    application_id = Column(Integer, ForeignKey("applications.id"), nullable=False)
    status = Column(String, nullable=False, default="pending")
    commit_sha = Column(String, nullable=False)
    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc), nullable=False)
    
    application = relationship("Application", back_populates="deployments")