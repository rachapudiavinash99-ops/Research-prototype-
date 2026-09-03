from sqlalchemy.orm import Session
from .models import PublicHealthExperiment, PublicHealthFinding, PublicHealthDataPoint
from .schemas import PublicHealthExperimentCreate, PublicHealthExperimentUpdate, PublicHealthFindingCreate, PublicHealthDataPointCreate
from typing import List, Optional

class PublicHealthService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[PublicHealthExperiment]:
        return self.db.query(PublicHealthExperiment).filter(PublicHealthExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[PublicHealthExperiment]:
        return self.db.query(PublicHealthExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: PublicHealthExperimentCreate) -> PublicHealthExperiment:
        db_exp = PublicHealthExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: PublicHealthExperimentUpdate) -> Optional[PublicHealthExperiment]:
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

    def create_finding(self, finding_in: PublicHealthFindingCreate) -> PublicHealthFinding:
        db_finding = PublicHealthFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[PublicHealthFinding]:
        return self.db.query(PublicHealthFinding).filter(PublicHealthFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: PublicHealthDataPointCreate) -> PublicHealthDataPoint:
        db_dp = PublicHealthDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[PublicHealthDataPoint]:
        return self.db.query(PublicHealthDataPoint).filter(PublicHealthDataPoint.experiment_id == experiment_id).all()
