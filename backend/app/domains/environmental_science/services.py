from sqlalchemy.orm import Session
from .models import EnvironmentalScienceExperiment, EnvironmentalScienceFinding, EnvironmentalScienceDataPoint
from .schemas import EnvironmentalScienceExperimentCreate, EnvironmentalScienceExperimentUpdate, EnvironmentalScienceFindingCreate, EnvironmentalScienceDataPointCreate
from typing import List, Optional

class EnvironmentalScienceService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[EnvironmentalScienceExperiment]:
        return self.db.query(EnvironmentalScienceExperiment).filter(EnvironmentalScienceExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[EnvironmentalScienceExperiment]:
        return self.db.query(EnvironmentalScienceExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: EnvironmentalScienceExperimentCreate) -> EnvironmentalScienceExperiment:
        db_exp = EnvironmentalScienceExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: EnvironmentalScienceExperimentUpdate) -> Optional[EnvironmentalScienceExperiment]:
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

    def create_finding(self, finding_in: EnvironmentalScienceFindingCreate) -> EnvironmentalScienceFinding:
        db_finding = EnvironmentalScienceFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[EnvironmentalScienceFinding]:
        return self.db.query(EnvironmentalScienceFinding).filter(EnvironmentalScienceFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: EnvironmentalScienceDataPointCreate) -> EnvironmentalScienceDataPoint:
        db_dp = EnvironmentalScienceDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[EnvironmentalScienceDataPoint]:
        return self.db.query(EnvironmentalScienceDataPoint).filter(EnvironmentalScienceDataPoint.experiment_id == experiment_id).all()
