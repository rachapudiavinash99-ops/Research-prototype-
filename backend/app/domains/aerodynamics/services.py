from sqlalchemy.orm import Session
from .models import AerodynamicsExperiment, AerodynamicsFinding, AerodynamicsDataPoint
from .schemas import AerodynamicsExperimentCreate, AerodynamicsExperimentUpdate, AerodynamicsFindingCreate, AerodynamicsDataPointCreate
from typing import List, Optional

class AerodynamicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AerodynamicsExperiment]:
        return self.db.query(AerodynamicsExperiment).filter(AerodynamicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AerodynamicsExperiment]:
        return self.db.query(AerodynamicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AerodynamicsExperimentCreate) -> AerodynamicsExperiment:
        db_exp = AerodynamicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AerodynamicsExperimentUpdate) -> Optional[AerodynamicsExperiment]:
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

    def create_finding(self, finding_in: AerodynamicsFindingCreate) -> AerodynamicsFinding:
        db_finding = AerodynamicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AerodynamicsFinding]:
        return self.db.query(AerodynamicsFinding).filter(AerodynamicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AerodynamicsDataPointCreate) -> AerodynamicsDataPoint:
        db_dp = AerodynamicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AerodynamicsDataPoint]:
        return self.db.query(AerodynamicsDataPoint).filter(AerodynamicsDataPoint.experiment_id == experiment_id).all()
