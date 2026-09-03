from sqlalchemy.orm import Session
from .models import CryptographyExperiment, CryptographyFinding, CryptographyDataPoint
from .schemas import CryptographyExperimentCreate, CryptographyExperimentUpdate, CryptographyFindingCreate, CryptographyDataPointCreate
from typing import List, Optional

class CryptographyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CryptographyExperiment]:
        return self.db.query(CryptographyExperiment).filter(CryptographyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CryptographyExperiment]:
        return self.db.query(CryptographyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CryptographyExperimentCreate) -> CryptographyExperiment:
        db_exp = CryptographyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CryptographyExperimentUpdate) -> Optional[CryptographyExperiment]:
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

    def create_finding(self, finding_in: CryptographyFindingCreate) -> CryptographyFinding:
        db_finding = CryptographyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CryptographyFinding]:
        return self.db.query(CryptographyFinding).filter(CryptographyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CryptographyDataPointCreate) -> CryptographyDataPoint:
        db_dp = CryptographyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CryptographyDataPoint]:
        return self.db.query(CryptographyDataPoint).filter(CryptographyDataPoint.experiment_id == experiment_id).all()
