from sqlalchemy.orm import Session
from .models import EpigenomicsExperiment, EpigenomicsFinding, EpigenomicsDataPoint
from .schemas import EpigenomicsExperimentCreate, EpigenomicsExperimentUpdate, EpigenomicsFindingCreate, EpigenomicsDataPointCreate
from typing import List, Optional

class EpigenomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[EpigenomicsExperiment]:
        return self.db.query(EpigenomicsExperiment).filter(EpigenomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[EpigenomicsExperiment]:
        return self.db.query(EpigenomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: EpigenomicsExperimentCreate) -> EpigenomicsExperiment:
        db_exp = EpigenomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: EpigenomicsExperimentUpdate) -> Optional[EpigenomicsExperiment]:
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

    def create_finding(self, finding_in: EpigenomicsFindingCreate) -> EpigenomicsFinding:
        db_finding = EpigenomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[EpigenomicsFinding]:
        return self.db.query(EpigenomicsFinding).filter(EpigenomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: EpigenomicsDataPointCreate) -> EpigenomicsDataPoint:
        db_dp = EpigenomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[EpigenomicsDataPoint]:
        return self.db.query(EpigenomicsDataPoint).filter(EpigenomicsDataPoint.experiment_id == experiment_id).all()
