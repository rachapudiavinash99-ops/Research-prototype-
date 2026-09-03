from sqlalchemy.orm import Session
from .models import ToxicologyExperiment, ToxicologyFinding, ToxicologyDataPoint
from .schemas import ToxicologyExperimentCreate, ToxicologyExperimentUpdate, ToxicologyFindingCreate, ToxicologyDataPointCreate
from typing import List, Optional

class ToxicologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ToxicologyExperiment]:
        return self.db.query(ToxicologyExperiment).filter(ToxicologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ToxicologyExperiment]:
        return self.db.query(ToxicologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ToxicologyExperimentCreate) -> ToxicologyExperiment:
        db_exp = ToxicologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ToxicologyExperimentUpdate) -> Optional[ToxicologyExperiment]:
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

    def create_finding(self, finding_in: ToxicologyFindingCreate) -> ToxicologyFinding:
        db_finding = ToxicologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ToxicologyFinding]:
        return self.db.query(ToxicologyFinding).filter(ToxicologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ToxicologyDataPointCreate) -> ToxicologyDataPoint:
        db_dp = ToxicologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ToxicologyDataPoint]:
        return self.db.query(ToxicologyDataPoint).filter(ToxicologyDataPoint.experiment_id == experiment_id).all()
