from sqlalchemy.orm import Session
from .models import ChemicalPhysicsExperiment, ChemicalPhysicsFinding, ChemicalPhysicsDataPoint
from .schemas import ChemicalPhysicsExperimentCreate, ChemicalPhysicsExperimentUpdate, ChemicalPhysicsFindingCreate, ChemicalPhysicsDataPointCreate
from typing import List, Optional

class ChemicalPhysicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ChemicalPhysicsExperiment]:
        return self.db.query(ChemicalPhysicsExperiment).filter(ChemicalPhysicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ChemicalPhysicsExperiment]:
        return self.db.query(ChemicalPhysicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ChemicalPhysicsExperimentCreate) -> ChemicalPhysicsExperiment:
        db_exp = ChemicalPhysicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ChemicalPhysicsExperimentUpdate) -> Optional[ChemicalPhysicsExperiment]:
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

    def create_finding(self, finding_in: ChemicalPhysicsFindingCreate) -> ChemicalPhysicsFinding:
        db_finding = ChemicalPhysicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ChemicalPhysicsFinding]:
        return self.db.query(ChemicalPhysicsFinding).filter(ChemicalPhysicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ChemicalPhysicsDataPointCreate) -> ChemicalPhysicsDataPoint:
        db_dp = ChemicalPhysicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ChemicalPhysicsDataPoint]:
        return self.db.query(ChemicalPhysicsDataPoint).filter(ChemicalPhysicsDataPoint.experiment_id == experiment_id).all()
