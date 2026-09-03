from sqlalchemy.orm import Session
from .models import NlpExperiment, NlpFinding, NlpDataPoint
from .schemas import NlpExperimentCreate, NlpExperimentUpdate, NlpFindingCreate, NlpDataPointCreate
from typing import List, Optional

class NlpService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[NlpExperiment]:
        return self.db.query(NlpExperiment).filter(NlpExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[NlpExperiment]:
        return self.db.query(NlpExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: NlpExperimentCreate) -> NlpExperiment:
        db_exp = NlpExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: NlpExperimentUpdate) -> Optional[NlpExperiment]:
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

    def create_finding(self, finding_in: NlpFindingCreate) -> NlpFinding:
        db_finding = NlpFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[NlpFinding]:
        return self.db.query(NlpFinding).filter(NlpFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: NlpDataPointCreate) -> NlpDataPoint:
        db_dp = NlpDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[NlpDataPoint]:
        return self.db.query(NlpDataPoint).filter(NlpDataPoint.experiment_id == experiment_id).all()
