from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class InorganicChemistryExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class InorganicChemistryExperimentCreate(InorganicChemistryExperimentBase):
    pass

class InorganicChemistryExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class InorganicChemistryExperimentResponse(InorganicChemistryExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class InorganicChemistryFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class InorganicChemistryFindingCreate(InorganicChemistryFindingBase):
    pass

class InorganicChemistryFindingResponse(InorganicChemistryFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class InorganicChemistryDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class InorganicChemistryDataPointCreate(InorganicChemistryDataPointBase):
    pass

class InorganicChemistryDataPointResponse(InorganicChemistryDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
