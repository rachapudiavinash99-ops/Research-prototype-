from sqlalchemy.orm import Session
from .models import BiotechnologyExperiment, BiotechnologyFinding, BiotechnologyDataPoint
from .schemas import BiotechnologyExperimentCreate, BiotechnologyExperimentUpdate, BiotechnologyFindingCreate, BiotechnologyDataPointCreate
from typing import List, Optional

class BiotechnologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[BiotechnologyExperiment]:
        return self.db.query(BiotechnologyExperiment).filter(BiotechnologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[BiotechnologyExperiment]:
        return self.db.query(BiotechnologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: BiotechnologyExperimentCreate) -> BiotechnologyExperiment:
        db_exp = BiotechnologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: BiotechnologyExperimentUpdate) -> Optional[BiotechnologyExperiment]:
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

    def create_finding(self, finding_in: BiotechnologyFindingCreate) -> BiotechnologyFinding:
        db_finding = BiotechnologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[BiotechnologyFinding]:
        return self.db.query(BiotechnologyFinding).filter(BiotechnologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: BiotechnologyDataPointCreate) -> BiotechnologyDataPoint:
        db_dp = BiotechnologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[BiotechnologyDataPoint]:
        return self.db.query(BiotechnologyDataPoint).filter(BiotechnologyDataPoint.experiment_id == experiment_id).all()
