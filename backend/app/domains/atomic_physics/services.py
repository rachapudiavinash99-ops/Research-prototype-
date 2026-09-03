from sqlalchemy.orm import Session
from .models import AtomicPhysicsExperiment, AtomicPhysicsFinding, AtomicPhysicsDataPoint
from .schemas import AtomicPhysicsExperimentCreate, AtomicPhysicsExperimentUpdate, AtomicPhysicsFindingCreate, AtomicPhysicsDataPointCreate
from typing import List, Optional

class AtomicPhysicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AtomicPhysicsExperiment]:
        return self.db.query(AtomicPhysicsExperiment).filter(AtomicPhysicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AtomicPhysicsExperiment]:
        return self.db.query(AtomicPhysicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AtomicPhysicsExperimentCreate) -> AtomicPhysicsExperiment:
        db_exp = AtomicPhysicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AtomicPhysicsExperimentUpdate) -> Optional[AtomicPhysicsExperiment]:
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

    def create_finding(self, finding_in: AtomicPhysicsFindingCreate) -> AtomicPhysicsFinding:
        db_finding = AtomicPhysicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AtomicPhysicsFinding]:
        return self.db.query(AtomicPhysicsFinding).filter(AtomicPhysicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AtomicPhysicsDataPointCreate) -> AtomicPhysicsDataPoint:
        db_dp = AtomicPhysicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AtomicPhysicsDataPoint]:
        return self.db.query(AtomicPhysicsDataPoint).filter(AtomicPhysicsDataPoint.experiment_id == experiment_id).all()
