from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class CybersecurityExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class CybersecurityExperimentCreate(CybersecurityExperimentBase):
    pass

class CybersecurityExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class CybersecurityExperimentResponse(CybersecurityExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class CybersecurityFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class CybersecurityFindingCreate(CybersecurityFindingBase):
    pass

class CybersecurityFindingResponse(CybersecurityFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class CybersecurityDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class CybersecurityDataPointCreate(CybersecurityDataPointBase):
    pass

class CybersecurityDataPointResponse(CybersecurityDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
