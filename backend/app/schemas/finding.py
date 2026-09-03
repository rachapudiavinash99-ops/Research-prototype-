from pydantic import BaseModel
from datetime import datetime
from typing import Optional
from app.models.finding import ConfidenceLevel

class FindingBase(BaseModel):
    title: str
    description: Optional[str] = None
    confidence: ConfidenceLevel = ConfidenceLevel.medium
    experiment_id: int

class FindingCreate(FindingBase):
    pass

class FindingResponse(FindingBase):
    id: int
    created_at: datetime
    class Config:
        from_attributes = True
