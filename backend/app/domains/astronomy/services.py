from sqlalchemy.orm import Session
from .models import AstronomyExperiment, AstronomyFinding, AstronomyDataPoint
from .schemas import AstronomyExperimentCreate, AstronomyExperimentUpdate, AstronomyFindingCreate, AstronomyDataPointCreate
from typing import List, Optional

class AstronomyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AstronomyExperiment]:
        return self.db.query(AstronomyExperiment).filter(AstronomyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AstronomyExperiment]:
        return self.db.query(AstronomyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AstronomyExperimentCreate) -> AstronomyExperiment:
        db_exp = AstronomyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AstronomyExperimentUpdate) -> Optional[AstronomyExperiment]:
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

    def create_finding(self, finding_in: AstronomyFindingCreate) -> AstronomyFinding:
        db_finding = AstronomyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AstronomyFinding]:
        return self.db.query(AstronomyFinding).filter(AstronomyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AstronomyDataPointCreate) -> AstronomyDataPoint:
        db_dp = AstronomyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AstronomyDataPoint]:
        return self.db.query(AstronomyDataPoint).filter(AstronomyDataPoint.experiment_id == experiment_id).all()
