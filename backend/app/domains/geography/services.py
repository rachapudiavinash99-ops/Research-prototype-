from sqlalchemy.orm import Session
from .models import GeographyExperiment, GeographyFinding, GeographyDataPoint
from .schemas import GeographyExperimentCreate, GeographyExperimentUpdate, GeographyFindingCreate, GeographyDataPointCreate
from typing import List, Optional

class GeographyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[GeographyExperiment]:
        return self.db.query(GeographyExperiment).filter(GeographyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[GeographyExperiment]:
        return self.db.query(GeographyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: GeographyExperimentCreate) -> GeographyExperiment:
        db_exp = GeographyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: GeographyExperimentUpdate) -> Optional[GeographyExperiment]:
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

    def create_finding(self, finding_in: GeographyFindingCreate) -> GeographyFinding:
        db_finding = GeographyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[GeographyFinding]:
        return self.db.query(GeographyFinding).filter(GeographyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: GeographyDataPointCreate) -> GeographyDataPoint:
        db_dp = GeographyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[GeographyDataPoint]:
        return self.db.query(GeographyDataPoint).filter(GeographyDataPoint.experiment_id == experiment_id).all()
