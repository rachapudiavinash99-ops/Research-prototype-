from sqlalchemy.orm import Session
from .models import ComputationalLinguisticsExperiment, ComputationalLinguisticsFinding, ComputationalLinguisticsDataPoint
from .schemas import ComputationalLinguisticsExperimentCreate, ComputationalLinguisticsExperimentUpdate, ComputationalLinguisticsFindingCreate, ComputationalLinguisticsDataPointCreate
from typing import List, Optional

class ComputationalLinguisticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ComputationalLinguisticsExperiment]:
        return self.db.query(ComputationalLinguisticsExperiment).filter(ComputationalLinguisticsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ComputationalLinguisticsExperiment]:
        return self.db.query(ComputationalLinguisticsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ComputationalLinguisticsExperimentCreate) -> ComputationalLinguisticsExperiment:
        db_exp = ComputationalLinguisticsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ComputationalLinguisticsExperimentUpdate) -> Optional[ComputationalLinguisticsExperiment]:
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

    def create_finding(self, finding_in: ComputationalLinguisticsFindingCreate) -> ComputationalLinguisticsFinding:
        db_finding = ComputationalLinguisticsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ComputationalLinguisticsFinding]:
        return self.db.query(ComputationalLinguisticsFinding).filter(ComputationalLinguisticsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ComputationalLinguisticsDataPointCreate) -> ComputationalLinguisticsDataPoint:
        db_dp = ComputationalLinguisticsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ComputationalLinguisticsDataPoint]:
        return self.db.query(ComputationalLinguisticsDataPoint).filter(ComputationalLinguisticsDataPoint.experiment_id == experiment_id).all()
