from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class MediaStudiesExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class MediaStudiesExperimentCreate(MediaStudiesExperimentBase):
    pass

class MediaStudiesExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class MediaStudiesExperimentResponse(MediaStudiesExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class MediaStudiesFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class MediaStudiesFindingCreate(MediaStudiesFindingBase):
    pass

class MediaStudiesFindingResponse(MediaStudiesFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class MediaStudiesDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class MediaStudiesDataPointCreate(MediaStudiesDataPointBase):
    pass

class MediaStudiesDataPointResponse(MediaStudiesDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
