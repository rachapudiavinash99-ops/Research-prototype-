from sqlalchemy.orm import Session
from .models import OpticsExperiment, OpticsFinding, OpticsDataPoint
from .schemas import OpticsExperimentCreate, OpticsExperimentUpdate, OpticsFindingCreate, OpticsDataPointCreate
from typing import List, Optional

class OpticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[OpticsExperiment]:
        return self.db.query(OpticsExperiment).filter(OpticsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[OpticsExperiment]:
        return self.db.query(OpticsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: OpticsExperimentCreate) -> OpticsExperiment:
        db_exp = OpticsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: OpticsExperimentUpdate) -> Optional[OpticsExperiment]:
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

    def create_finding(self, finding_in: OpticsFindingCreate) -> OpticsFinding:
        db_finding = OpticsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[OpticsFinding]:
        return self.db.query(OpticsFinding).filter(OpticsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: OpticsDataPointCreate) -> OpticsDataPoint:
        db_dp = OpticsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[OpticsDataPoint]:
        return self.db.query(OpticsDataPoint).filter(OpticsDataPoint.experiment_id == experiment_id).all()
