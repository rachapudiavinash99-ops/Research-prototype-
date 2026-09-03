from sqlalchemy.orm import Session
from .models import ComputerVisionExperiment, ComputerVisionFinding, ComputerVisionDataPoint
from .schemas import ComputerVisionExperimentCreate, ComputerVisionExperimentUpdate, ComputerVisionFindingCreate, ComputerVisionDataPointCreate
from typing import List, Optional

class ComputerVisionService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ComputerVisionExperiment]:
        return self.db.query(ComputerVisionExperiment).filter(ComputerVisionExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ComputerVisionExperiment]:
        return self.db.query(ComputerVisionExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ComputerVisionExperimentCreate) -> ComputerVisionExperiment:
        db_exp = ComputerVisionExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ComputerVisionExperimentUpdate) -> Optional[ComputerVisionExperiment]:
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

    def create_finding(self, finding_in: ComputerVisionFindingCreate) -> ComputerVisionFinding:
        db_finding = ComputerVisionFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ComputerVisionFinding]:
        return self.db.query(ComputerVisionFinding).filter(ComputerVisionFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ComputerVisionDataPointCreate) -> ComputerVisionDataPoint:
        db_dp = ComputerVisionDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ComputerVisionDataPoint]:
        return self.db.query(ComputerVisionDataPoint).filter(ComputerVisionDataPoint.experiment_id == experiment_id).all()
