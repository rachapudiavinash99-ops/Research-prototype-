from sqlalchemy.orm import Session
from .models import CombinatoricsExperiment, CombinatoricsFinding, CombinatoricsDataPoint
from .schemas import CombinatoricsExperimentCreate, CombinatoricsExperimentUpdate, CombinatoricsFindingCreate, CombinatoricsDataPointCreate
from typing import List, Optional

class CombinatoricsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CombinatoricsExperiment]:
        return self.db.query(CombinatoricsExperiment).filter(CombinatoricsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CombinatoricsExperiment]:
        return self.db.query(CombinatoricsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CombinatoricsExperimentCreate) -> CombinatoricsExperiment:
        db_exp = CombinatoricsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CombinatoricsExperimentUpdate) -> Optional[CombinatoricsExperiment]:
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

    def create_finding(self, finding_in: CombinatoricsFindingCreate) -> CombinatoricsFinding:
        db_finding = CombinatoricsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CombinatoricsFinding]:
        return self.db.query(CombinatoricsFinding).filter(CombinatoricsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CombinatoricsDataPointCreate) -> CombinatoricsDataPoint:
        db_dp = CombinatoricsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CombinatoricsDataPoint]:
        return self.db.query(CombinatoricsDataPoint).filter(CombinatoricsDataPoint.experiment_id == experiment_id).all()
