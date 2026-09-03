from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class GeographyExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class GeographyExperimentCreate(GeographyExperimentBase):
    pass

class GeographyExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class GeographyExperimentResponse(GeographyExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class GeographyFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class GeographyFindingCreate(GeographyFindingBase):
    pass

class GeographyFindingResponse(GeographyFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class GeographyDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class GeographyDataPointCreate(GeographyDataPointBase):
    pass

class GeographyDataPointResponse(GeographyDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
