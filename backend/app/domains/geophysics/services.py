from sqlalchemy.orm import Session
from .models import GeophysicsExperiment, GeophysicsFinding, GeophysicsDataPoint
from .schemas import GeophysicsExperimentCreate, GeophysicsExperimentUpdate, GeophysicsFindingCreate, GeophysicsDataPointCreate
from typing import List, Optional

class GeophysicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[GeophysicsExperiment]:
        return self.db.query(GeophysicsExperiment).filter(GeophysicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[GeophysicsExperiment]:
        return self.db.query(GeophysicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: GeophysicsExperimentCreate) -> GeophysicsExperiment:
        db_exp = GeophysicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: GeophysicsExperimentUpdate) -> Optional[GeophysicsExperiment]:
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

    def create_finding(self, finding_in: GeophysicsFindingCreate) -> GeophysicsFinding:
        db_finding = GeophysicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[GeophysicsFinding]:
        return self.db.query(GeophysicsFinding).filter(GeophysicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: GeophysicsDataPointCreate) -> GeophysicsDataPoint:
        db_dp = GeophysicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[GeophysicsDataPoint]:
        return self.db.query(GeophysicsDataPoint).filter(GeophysicsDataPoint.experiment_id == experiment_id).all()
