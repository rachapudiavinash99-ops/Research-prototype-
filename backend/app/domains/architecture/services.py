from sqlalchemy.orm import Session
from .models import ArchitectureExperiment, ArchitectureFinding, ArchitectureDataPoint
from .schemas import ArchitectureExperimentCreate, ArchitectureExperimentUpdate, ArchitectureFindingCreate, ArchitectureDataPointCreate
from typing import List, Optional

class ArchitectureService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ArchitectureExperiment]:
        return self.db.query(ArchitectureExperiment).filter(ArchitectureExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ArchitectureExperiment]:
        return self.db.query(ArchitectureExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ArchitectureExperimentCreate) -> ArchitectureExperiment:
        db_exp = ArchitectureExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ArchitectureExperimentUpdate) -> Optional[ArchitectureExperiment]:
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

    def create_finding(self, finding_in: ArchitectureFindingCreate) -> ArchitectureFinding:
        db_finding = ArchitectureFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ArchitectureFinding]:
        return self.db.query(ArchitectureFinding).filter(ArchitectureFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ArchitectureDataPointCreate) -> ArchitectureDataPoint:
        db_dp = ArchitectureDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ArchitectureDataPoint]:
        return self.db.query(ArchitectureDataPoint).filter(ArchitectureDataPoint.experiment_id == experiment_id).all()
