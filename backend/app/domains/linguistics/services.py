from sqlalchemy.orm import Session
from .models import LinguisticsExperiment, LinguisticsFinding, LinguisticsDataPoint
from .schemas import LinguisticsExperimentCreate, LinguisticsExperimentUpdate, LinguisticsFindingCreate, LinguisticsDataPointCreate
from typing import List, Optional

class LinguisticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[LinguisticsExperiment]:
        return self.db.query(LinguisticsExperiment).filter(LinguisticsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[LinguisticsExperiment]:
        return self.db.query(LinguisticsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: LinguisticsExperimentCreate) -> LinguisticsExperiment:
        db_exp = LinguisticsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: LinguisticsExperimentUpdate) -> Optional[LinguisticsExperiment]:
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

    def create_finding(self, finding_in: LinguisticsFindingCreate) -> LinguisticsFinding:
        db_finding = LinguisticsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[LinguisticsFinding]:
        return self.db.query(LinguisticsFinding).filter(LinguisticsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: LinguisticsDataPointCreate) -> LinguisticsDataPoint:
        db_dp = LinguisticsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[LinguisticsDataPoint]:
        return self.db.query(LinguisticsDataPoint).filter(LinguisticsDataPoint.experiment_id == experiment_id).all()
