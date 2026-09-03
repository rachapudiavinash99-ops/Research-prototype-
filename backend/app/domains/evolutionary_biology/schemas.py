from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class EvolutionaryBiologyExperimentBase(BaseModel):
    title: str = Field(..., title="Title of the experiment")
    description: Optional[str] = None
    methodology: Optional[str] = None
    hypothesis: Optional[str] = None
    variables: Optional[str] = None
    expected_outcome: Optional[str] = None
    success_rate: float = 0.0
    is_peer_reviewed: bool = False

class EvolutionaryBiologyExperimentCreate(EvolutionaryBiologyExperimentBase):
    pass

class EvolutionaryBiologyExperimentUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    actual_outcome: Optional[str] = None
    success_rate: Optional[float] = None
    is_peer_reviewed: Optional[bool] = None

class EvolutionaryBiologyExperimentResponse(EvolutionaryBiologyExperimentBase):
    id: int
    actual_outcome: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime]
    
    class Config:
        from_attributes = True

class EvolutionaryBiologyFindingBase(BaseModel):
    experiment_id: int
    conclusion: str
    confidence_score: float = 0.0
    limitations: Optional[str] = None
    future_work: Optional[str] = None

class EvolutionaryBiologyFindingCreate(EvolutionaryBiologyFindingBase):
    pass

class EvolutionaryBiologyFindingResponse(EvolutionaryBiologyFindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
        
class EvolutionaryBiologyDataPointBase(BaseModel):
    experiment_id: int
    metric_name: str
    metric_value: float

class EvolutionaryBiologyDataPointCreate(EvolutionaryBiologyDataPointBase):
    pass

class EvolutionaryBiologyDataPointResponse(EvolutionaryBiologyDataPointBase):
    id: int
    timestamp: datetime
    class Config:
        from_attributes = True
