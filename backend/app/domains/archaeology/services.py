from sqlalchemy.orm import Session
from .models import ArchaeologyExperiment, ArchaeologyFinding, ArchaeologyDataPoint
from .schemas import ArchaeologyExperimentCreate, ArchaeologyExperimentUpdate, ArchaeologyFindingCreate, ArchaeologyDataPointCreate
from typing import List, Optional

class ArchaeologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ArchaeologyExperiment]:
        return self.db.query(ArchaeologyExperiment).filter(ArchaeologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ArchaeologyExperiment]:
        return self.db.query(ArchaeologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ArchaeologyExperimentCreate) -> ArchaeologyExperiment:
        db_exp = ArchaeologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ArchaeologyExperimentUpdate) -> Optional[ArchaeologyExperiment]:
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

    def create_finding(self, finding_in: ArchaeologyFindingCreate) -> ArchaeologyFinding:
        db_finding = ArchaeologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ArchaeologyFinding]:
        return self.db.query(ArchaeologyFinding).filter(ArchaeologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ArchaeologyDataPointCreate) -> ArchaeologyDataPoint:
        db_dp = ArchaeologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ArchaeologyDataPoint]:
        return self.db.query(ArchaeologyDataPoint).filter(ArchaeologyDataPoint.experiment_id == experiment_id).all()
