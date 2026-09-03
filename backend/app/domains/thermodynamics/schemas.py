from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ThermodynamicsExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class ThermodynamicsExperimentCreate(ThermodynamicsExperimentBase):
    pass

class ThermodynamicsExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class ThermodynamicsExperimentResponse(ThermodynamicsExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ThermodynamicsFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class ThermodynamicsFindingCreate(ThermodynamicsFindingBase):
    pass

class ThermodynamicsFindingResponse(ThermodynamicsFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class ThermodynamicsDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class ThermodynamicsDataPointCreate(ThermodynamicsDataPointBase):
    pass

class ThermodynamicsDataPointResponse(ThermodynamicsDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
