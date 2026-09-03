from sqlalchemy.orm import Session
from .models import CriminologyExperiment, CriminologyFinding, CriminologyDataPoint
from .schemas import CriminologyExperimentCreate, CriminologyExperimentUpdate, CriminologyFindingCreate, CriminologyDataPointCreate
from typing import List, Optional

class CriminologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CriminologyExperiment]:
        return self.db.query(CriminologyExperiment).filter(CriminologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CriminologyExperiment]:
        return self.db.query(CriminologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CriminologyExperimentCreate) -> CriminologyExperiment:
        db_exp = CriminologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CriminologyExperimentUpdate) -> Optional[CriminologyExperiment]:
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

    def create_finding(self, finding_in: CriminologyFindingCreate) -> CriminologyFinding:
        db_finding = CriminologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CriminologyFinding]:
        return self.db.query(CriminologyFinding).filter(CriminologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CriminologyDataPointCreate) -> CriminologyDataPoint:
        db_dp = CriminologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CriminologyDataPoint]:
        return self.db.query(CriminologyDataPoint).filter(CriminologyDataPoint.experiment_id == experiment_id).all()
