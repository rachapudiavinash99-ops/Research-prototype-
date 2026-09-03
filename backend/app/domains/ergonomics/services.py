from sqlalchemy.orm import Session
from .models import ErgonomicsExperiment, ErgonomicsFinding, ErgonomicsDataPoint
from .schemas import ErgonomicsExperimentCreate, ErgonomicsExperimentUpdate, ErgonomicsFindingCreate, ErgonomicsDataPointCreate
from typing import List, Optional

class ErgonomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ErgonomicsExperiment]:
        return self.db.query(ErgonomicsExperiment).filter(ErgonomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ErgonomicsExperiment]:
        return self.db.query(ErgonomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ErgonomicsExperimentCreate) -> ErgonomicsExperiment:
        db_exp = ErgonomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ErgonomicsExperimentUpdate) -> Optional[ErgonomicsExperiment]:
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

    def create_finding(self, finding_in: ErgonomicsFindingCreate) -> ErgonomicsFinding:
        db_finding = ErgonomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ErgonomicsFinding]:
        return self.db.query(ErgonomicsFinding).filter(ErgonomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ErgonomicsDataPointCreate) -> ErgonomicsDataPoint:
        db_dp = ErgonomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ErgonomicsDataPoint]:
        return self.db.query(ErgonomicsDataPoint).filter(ErgonomicsDataPoint.experiment_id == experiment_id).all()
