from sqlalchemy.orm import Session
from .models import GeometryExperiment, GeometryFinding, GeometryDataPoint
from .schemas import GeometryExperimentCreate, GeometryExperimentUpdate, GeometryFindingCreate, GeometryDataPointCreate
from typing import List, Optional

class GeometryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[GeometryExperiment]:
        return self.db.query(GeometryExperiment).filter(GeometryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[GeometryExperiment]:
        return self.db.query(GeometryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: GeometryExperimentCreate) -> GeometryExperiment:
        db_exp = GeometryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: GeometryExperimentUpdate) -> Optional[GeometryExperiment]:
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

    def create_finding(self, finding_in: GeometryFindingCreate) -> GeometryFinding:
        db_finding = GeometryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[GeometryFinding]:
        return self.db.query(GeometryFinding).filter(GeometryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: GeometryDataPointCreate) -> GeometryDataPoint:
        db_dp = GeometryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[GeometryDataPoint]:
        return self.db.query(GeometryDataPoint).filter(GeometryDataPoint.experiment_id == experiment_id).all()
