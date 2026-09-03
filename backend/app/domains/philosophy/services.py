from sqlalchemy.orm import Session
from .models import PhilosophyExperiment, PhilosophyFinding, PhilosophyDataPoint
from .schemas import PhilosophyExperimentCreate, PhilosophyExperimentUpdate, PhilosophyFindingCreate, PhilosophyDataPointCreate
from typing import List, Optional

class PhilosophyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[PhilosophyExperiment]:
        return self.db.query(PhilosophyExperiment).filter(PhilosophyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[PhilosophyExperiment]:
        return self.db.query(PhilosophyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: PhilosophyExperimentCreate) -> PhilosophyExperiment:
        db_exp = PhilosophyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: PhilosophyExperimentUpdate) -> Optional[PhilosophyExperiment]:
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

    def create_finding(self, finding_in: PhilosophyFindingCreate) -> PhilosophyFinding:
        db_finding = PhilosophyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[PhilosophyFinding]:
        return self.db.query(PhilosophyFinding).filter(PhilosophyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: PhilosophyDataPointCreate) -> PhilosophyDataPoint:
        db_dp = PhilosophyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[PhilosophyDataPoint]:
        return self.db.query(PhilosophyDataPoint).filter(PhilosophyDataPoint.experiment_id == experiment_id).all()
