from sqlalchemy import Column, Integer, String, Text, Float, Boolean, DateTime
from sqlalchemy.sql import func
from app.db.base import Base

class HistoryExperiment(Base):
    __tablename__ = "history_experiments"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(Text)
    methodology = Column(Text)
    hypothesis = Column(Text)
    variables = Column(Text)
    expected_outcome = Column(Text)
    actual_outcome = Column(Text)
    success_rate = Column(Float, default=0.0)
    is_peer_reviewed = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

class HistoryFinding(Base):
    __tablename__ = "history_findings"
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, index=True)
    conclusion = Column(Text)
    confidence_score = Column(Float, default=0.0)
    limitations = Column(Text)
    future_work = Column(Text)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
class HistoryDataPoint(Base):
    __tablename__ = "history_datapoints"
    id = Column(Integer, primary_key=True, index=True)
    experiment_id = Column(Integer, index=True)
    metric_name = Column(String)
    metric_value = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
