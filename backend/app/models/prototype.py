from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class PrototypeStatus(str, enum.Enum):
    idea = "idea"
    design = "design"
    development = "development"
    experiment = "experiment"
    testing = "testing"
    evaluation = "evaluation"
    accepted = "accepted"
    rejected = "rejected"
    archived = "archived"

class ExperimentStatus(str, enum.Enum):
    planned = "planned"
    running = "running"
    successful = "successful"
    failed = "failed"
    inconclusive = "inconclusive"

class Prototype(Base):
    __tablename__ = "prototypes"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    version = Column(String, nullable=False)
    description = Column(Text)
    project_id = Column(Integer, ForeignKey("projects.id"))
    status = Column(Enum(PrototypeStatus), default=PrototypeStatus.idea)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    project = relationship("Project")

class Experiment(Base):
    __tablename__ = "experiments"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    objective = Column(Text)
    prototype_id = Column(Integer, ForeignKey("prototypes.id"))
    status = Column(Enum(ExperimentStatus), default=ExperimentStatus.planned)
    result_metrics = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    prototype = relationship("Prototype")
