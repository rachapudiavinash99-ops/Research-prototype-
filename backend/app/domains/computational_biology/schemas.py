from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class ComputationalBiologyExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class ComputationalBiologyExperimentCreate(ComputationalBiologyExperimentBase):
    pass

class ComputationalBiologyExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class ComputationalBiologyExperimentResponse(ComputationalBiologyExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class ComputationalBiologyFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class ComputationalBiologyFindingCreate(ComputationalBiologyFindingBase):
    pass

class ComputationalBiologyFindingResponse(ComputationalBiologyFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class ComputationalBiologyDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class ComputationalBiologyDataPointCreate(ComputationalBiologyDataPointBase):
    pass

class ComputationalBiologyDataPointResponse(ComputationalBiologyDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
