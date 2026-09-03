from sqlalchemy.orm import Session
from .models import ThermodynamicsExperiment, ThermodynamicsFinding, ThermodynamicsDataPoint
from .schemas import ThermodynamicsExperimentCreate, ThermodynamicsExperimentUpdate, ThermodynamicsFindingCreate, ThermodynamicsDataPointCreate
from typing import List, Optional

class ThermodynamicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ThermodynamicsExperiment]:
        return self.db.query(ThermodynamicsExperiment).filter(ThermodynamicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ThermodynamicsExperiment]:
        return self.db.query(ThermodynamicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ThermodynamicsExperimentCreate) -> ThermodynamicsExperiment:
        db_exp = ThermodynamicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ThermodynamicsExperimentUpdate) -> Optional[ThermodynamicsExperiment]:
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

    def create_finding(self, finding_in: ThermodynamicsFindingCreate) -> ThermodynamicsFinding:
        db_finding = ThermodynamicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ThermodynamicsFinding]:
        return self.db.query(ThermodynamicsFinding).filter(ThermodynamicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ThermodynamicsDataPointCreate) -> ThermodynamicsDataPoint:
        db_dp = ThermodynamicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ThermodynamicsDataPoint]:
        return self.db.query(ThermodynamicsDataPoint).filter(ThermodynamicsDataPoint.experiment_id == experiment_id).all()
