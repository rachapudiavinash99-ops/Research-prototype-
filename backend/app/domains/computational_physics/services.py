from sqlalchemy.orm import Session
from .models import ComputationalPhysicsExperiment, ComputationalPhysicsFinding, ComputationalPhysicsDataPoint
from .schemas import ComputationalPhysicsExperimentCreate, ComputationalPhysicsExperimentUpdate, ComputationalPhysicsFindingCreate, ComputationalPhysicsDataPointCreate
from typing import List, Optional

class ComputationalPhysicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ComputationalPhysicsExperiment]:
        return self.db.query(ComputationalPhysicsExperiment).filter(ComputationalPhysicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ComputationalPhysicsExperiment]:
        return self.db.query(ComputationalPhysicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ComputationalPhysicsExperimentCreate) -> ComputationalPhysicsExperiment:
        db_exp = ComputationalPhysicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ComputationalPhysicsExperimentUpdate) -> Optional[ComputationalPhysicsExperiment]:
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

    def create_finding(self, finding_in: ComputationalPhysicsFindingCreate) -> ComputationalPhysicsFinding:
        db_finding = ComputationalPhysicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ComputationalPhysicsFinding]:
        return self.db.query(ComputationalPhysicsFinding).filter(ComputationalPhysicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ComputationalPhysicsDataPointCreate) -> ComputationalPhysicsDataPoint:
        db_dp = ComputationalPhysicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ComputationalPhysicsDataPoint]:
        return self.db.query(ComputationalPhysicsDataPoint).filter(ComputationalPhysicsDataPoint.experiment_id == experiment_id).all()
