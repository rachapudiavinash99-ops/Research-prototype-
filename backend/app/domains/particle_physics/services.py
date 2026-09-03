from sqlalchemy.orm import Session
from .models import ParticlePhysicsExperiment, ParticlePhysicsFinding, ParticlePhysicsDataPoint
from .schemas import ParticlePhysicsExperimentCreate, ParticlePhysicsExperimentUpdate, ParticlePhysicsFindingCreate, ParticlePhysicsDataPointCreate
from typing import List, Optional

class ParticlePhysicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ParticlePhysicsExperiment]:
        return self.db.query(ParticlePhysicsExperiment).filter(ParticlePhysicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ParticlePhysicsExperiment]:
        return self.db.query(ParticlePhysicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ParticlePhysicsExperimentCreate) -> ParticlePhysicsExperiment:
        db_exp = ParticlePhysicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ParticlePhysicsExperimentUpdate) -> Optional[ParticlePhysicsExperiment]:
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

    def create_finding(self, finding_in: ParticlePhysicsFindingCreate) -> ParticlePhysicsFinding:
        db_finding = ParticlePhysicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ParticlePhysicsFinding]:
        return self.db.query(ParticlePhysicsFinding).filter(ParticlePhysicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ParticlePhysicsDataPointCreate) -> ParticlePhysicsDataPoint:
        db_dp = ParticlePhysicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ParticlePhysicsDataPoint]:
        return self.db.query(ParticlePhysicsDataPoint).filter(ParticlePhysicsDataPoint.experiment_id == experiment_id).all()
