from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.prototype import PrototypeStatus, ExperimentStatus

class PrototypeBase(BaseModel):
    name: str
    version: str
    description: Optional[str] = None
    project_id: int
    status: PrototypeStatus = PrototypeStatus.idea

class PrototypeCreate(PrototypeBase):
    pass

class PrototypeResponse(PrototypeBase):
    id: int
    created_at: datetime
    updated_at: Optional[datetime]
    class Config:
        from_attributes = True

class ExperimentBase(BaseModel):
    name: str
    objective: Optional[str] = None
    prototype_id: int
    status: ExperimentStatus = ExperimentStatus.planned

class ExperimentCreate(ExperimentBase):
    pass

class ExperimentResponse(ExperimentBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
