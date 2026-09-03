from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class EpidemiologyExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class EpidemiologyExperimentCreate(EpidemiologyExperimentBase):
    pass

class EpidemiologyExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class EpidemiologyExperimentResponse(EpidemiologyExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class EpidemiologyFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class EpidemiologyFindingCreate(EpidemiologyFindingBase):
    pass

class EpidemiologyFindingResponse(EpidemiologyFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class EpidemiologyDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class EpidemiologyDataPointCreate(EpidemiologyDataPointBase):
    pass

class EpidemiologyDataPointResponse(EpidemiologyDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
