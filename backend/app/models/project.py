from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Enum, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.session import Base
import enum

class ProjectStatus(str, enum.Enum):
    planning = "planning"
    active = "active"
    experimenting = "experimenting"
    under_review = "under_review"
    completed = "completed"
    archived = "archived"

project_members = Table(
    'project_members', Base.metadata,
    Column('project_id', Integer, ForeignKey('projects.id')),
    Column('user_id', Integer, ForeignKey('users.id'))
)

class Topic(Base):
    __tablename__ = "topics"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    projects = relationship("Project", back_populates="topic")

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    description = Column(Text)
    topic_id = Column(Integer, ForeignKey("topics.id"))
    status = Column(Enum(ProjectStatus), default=ProjectStatus.planning)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    owner = relationship("User")
    topic = relationship("Topic", back_populates="projects")
    members = relationship("User", secondary=project_members)
