from sqlalchemy.orm import Session
from .models import CondensedMatterPhysicsExperiment, CondensedMatterPhysicsFinding, CondensedMatterPhysicsDataPoint
from .schemas import CondensedMatterPhysicsExperimentCreate, CondensedMatterPhysicsExperimentUpdate, CondensedMatterPhysicsFindingCreate, CondensedMatterPhysicsDataPointCreate
from typing import List, Optional

class CondensedMatterPhysicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CondensedMatterPhysicsExperiment]:
        return self.db.query(CondensedMatterPhysicsExperiment).filter(CondensedMatterPhysicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CondensedMatterPhysicsExperiment]:
        return self.db.query(CondensedMatterPhysicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CondensedMatterPhysicsExperimentCreate) -> CondensedMatterPhysicsExperiment:
        db_exp = CondensedMatterPhysicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CondensedMatterPhysicsExperimentUpdate) -> Optional[CondensedMatterPhysicsExperiment]:
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

    def create_finding(self, finding_in: CondensedMatterPhysicsFindingCreate) -> CondensedMatterPhysicsFinding:
        db_finding = CondensedMatterPhysicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CondensedMatterPhysicsFinding]:
        return self.db.query(CondensedMatterPhysicsFinding).filter(CondensedMatterPhysicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CondensedMatterPhysicsDataPointCreate) -> CondensedMatterPhysicsDataPoint:
        db_dp = CondensedMatterPhysicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CondensedMatterPhysicsDataPoint]:
        return self.db.query(CondensedMatterPhysicsDataPoint).filter(CondensedMatterPhysicsDataPoint.experiment_id == experiment_id).all()
