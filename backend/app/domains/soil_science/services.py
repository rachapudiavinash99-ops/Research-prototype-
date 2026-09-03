from sqlalchemy.orm import Session
from .models import SoilScienceExperiment, SoilScienceFinding, SoilScienceDataPoint
from .schemas import SoilScienceExperimentCreate, SoilScienceExperimentUpdate, SoilScienceFindingCreate, SoilScienceDataPointCreate
from typing import List, Optional

class SoilScienceService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SoilScienceExperiment]:
        return self.db.query(SoilScienceExperiment).filter(SoilScienceExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SoilScienceExperiment]:
        return self.db.query(SoilScienceExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SoilScienceExperimentCreate) -> SoilScienceExperiment:
        db_exp = SoilScienceExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SoilScienceExperimentUpdate) -> Optional[SoilScienceExperiment]:
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

    def create_finding(self, finding_in: SoilScienceFindingCreate) -> SoilScienceFinding:
        db_finding = SoilScienceFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SoilScienceFinding]:
        return self.db.query(SoilScienceFinding).filter(SoilScienceFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SoilScienceDataPointCreate) -> SoilScienceDataPoint:
        db_dp = SoilScienceDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SoilScienceDataPoint]:
        return self.db.query(SoilScienceDataPoint).filter(SoilScienceDataPoint.experiment_id == experiment_id).all()
