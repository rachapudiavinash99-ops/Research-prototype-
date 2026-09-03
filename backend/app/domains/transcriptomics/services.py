from sqlalchemy.orm import Session
from .models import TranscriptomicsExperiment, TranscriptomicsFinding, TranscriptomicsDataPoint
from .schemas import TranscriptomicsExperimentCreate, TranscriptomicsExperimentUpdate, TranscriptomicsFindingCreate, TranscriptomicsDataPointCreate
from typing import List, Optional

class TranscriptomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[TranscriptomicsExperiment]:
        return self.db.query(TranscriptomicsExperiment).filter(TranscriptomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[TranscriptomicsExperiment]:
        return self.db.query(TranscriptomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: TranscriptomicsExperimentCreate) -> TranscriptomicsExperiment:
        db_exp = TranscriptomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: TranscriptomicsExperimentUpdate) -> Optional[TranscriptomicsExperiment]:
        db_exp = self.get_experiment(experiment_id)
        if not db_exp:
            return None
        update_data = exp_in.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_exp, field, value)
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def delete_experiment(self, experiment_id: int) -> bool:
        db_exp = self.get_experiment(experiment_id)
        if not db_exp:
            return False
        self.db.delete(db_exp)
        self.db.commit()
        return True

    def create_finding(self, finding_in: TranscriptomicsFindingCreate) -> TranscriptomicsFinding:
        db_finding = TranscriptomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[TranscriptomicsFinding]:
        return self.db.query(TranscriptomicsFinding).filter(TranscriptomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: TranscriptomicsDataPointCreate) -> TranscriptomicsDataPoint:
        db_dp = TranscriptomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[TranscriptomicsDataPoint]:
        return self.db.query(TranscriptomicsDataPoint).filter(TranscriptomicsDataPoint.experiment_id == experiment_id).all()
