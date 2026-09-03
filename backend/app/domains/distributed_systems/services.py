from sqlalchemy.orm import Session
from .models import DistributedSystemsExperiment, DistributedSystemsFinding, DistributedSystemsDataPoint
from .schemas import DistributedSystemsExperimentCreate, DistributedSystemsExperimentUpdate, DistributedSystemsFindingCreate, DistributedSystemsDataPointCreate
from typing import List, Optional

class DistributedSystemsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DistributedSystemsExperiment]:
        return self.db.query(DistributedSystemsExperiment).filter(DistributedSystemsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DistributedSystemsExperiment]:
        return self.db.query(DistributedSystemsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DistributedSystemsExperimentCreate) -> DistributedSystemsExperiment:
        db_exp = DistributedSystemsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DistributedSystemsExperimentUpdate) -> Optional[DistributedSystemsExperiment]:
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

    def create_finding(self, finding_in: DistributedSystemsFindingCreate) -> DistributedSystemsFinding:
        db_finding = DistributedSystemsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DistributedSystemsFinding]:
        return self.db.query(DistributedSystemsFinding).filter(DistributedSystemsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DistributedSystemsDataPointCreate) -> DistributedSystemsDataPoint:
        db_dp = DistributedSystemsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DistributedSystemsDataPoint]:
        return self.db.query(DistributedSystemsDataPoint).filter(DistributedSystemsDataPoint.experiment_id == experiment_id).all()
