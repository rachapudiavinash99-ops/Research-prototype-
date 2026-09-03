from sqlalchemy.orm import Session
from .models import LiteratureExperiment, LiteratureFinding, LiteratureDataPoint
from .schemas import LiteratureExperimentCreate, LiteratureExperimentUpdate, LiteratureFindingCreate, LiteratureDataPointCreate
from typing import List, Optional

class LiteratureService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[LiteratureExperiment]:
        return self.db.query(LiteratureExperiment).filter(LiteratureExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[LiteratureExperiment]:
        return self.db.query(LiteratureExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: LiteratureExperimentCreate) -> LiteratureExperiment:
        db_exp = LiteratureExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: LiteratureExperimentUpdate) -> Optional[LiteratureExperiment]:
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

    def create_finding(self, finding_in: LiteratureFindingCreate) -> LiteratureFinding:
        db_finding = LiteratureFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[LiteratureFinding]:
        return self.db.query(LiteratureFinding).filter(LiteratureFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: LiteratureDataPointCreate) -> LiteratureDataPoint:
        db_dp = LiteratureDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[LiteratureDataPoint]:
        return self.db.query(LiteratureDataPoint).filter(LiteratureDataPoint.experiment_id == experiment_id).all()
