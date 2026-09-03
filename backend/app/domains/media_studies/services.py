from sqlalchemy.orm import Session
from .models import MediaStudiesExperiment, MediaStudiesFinding, MediaStudiesDataPoint
from .schemas import MediaStudiesExperimentCreate, MediaStudiesExperimentUpdate, MediaStudiesFindingCreate, MediaStudiesDataPointCreate
from typing import List, Optional

class MediaStudiesService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MediaStudiesExperiment]:
        return self.db.query(MediaStudiesExperiment).filter(MediaStudiesExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MediaStudiesExperiment]:
        return self.db.query(MediaStudiesExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MediaStudiesExperimentCreate) -> MediaStudiesExperiment:
        db_exp = MediaStudiesExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MediaStudiesExperimentUpdate) -> Optional[MediaStudiesExperiment]:
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

    def create_finding(self, finding_in: MediaStudiesFindingCreate) -> MediaStudiesFinding:
        db_finding = MediaStudiesFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MediaStudiesFinding]:
        return self.db.query(MediaStudiesFinding).filter(MediaStudiesFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MediaStudiesDataPointCreate) -> MediaStudiesDataPoint:
        db_dp = MediaStudiesDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MediaStudiesDataPoint]:
        return self.db.query(MediaStudiesDataPoint).filter(MediaStudiesDataPoint.experiment_id == experiment_id).all()
