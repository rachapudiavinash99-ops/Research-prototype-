from sqlalchemy.orm import Session
from .models import DeepLearningExperiment, DeepLearningFinding, DeepLearningDataPoint
from .schemas import DeepLearningExperimentCreate, DeepLearningExperimentUpdate, DeepLearningFindingCreate, DeepLearningDataPointCreate
from typing import List, Optional

class DeepLearningService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DeepLearningExperiment]:
        return self.db.query(DeepLearningExperiment).filter(DeepLearningExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DeepLearningExperiment]:
        return self.db.query(DeepLearningExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DeepLearningExperimentCreate) -> DeepLearningExperiment:
        db_exp = DeepLearningExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DeepLearningExperimentUpdate) -> Optional[DeepLearningExperiment]:
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

    def create_finding(self, finding_in: DeepLearningFindingCreate) -> DeepLearningFinding:
        db_finding = DeepLearningFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DeepLearningFinding]:
        return self.db.query(DeepLearningFinding).filter(DeepLearningFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DeepLearningDataPointCreate) -> DeepLearningDataPoint:
        db_dp = DeepLearningDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DeepLearningDataPoint]:
        return self.db.query(DeepLearningDataPoint).filter(DeepLearningDataPoint.experiment_id == experiment_id).all()
