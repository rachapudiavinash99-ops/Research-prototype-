from sqlalchemy.orm import Session
from .models import MachineLearningExperiment, MachineLearningFinding, MachineLearningDataPoint
from .schemas import MachineLearningExperimentCreate, MachineLearningExperimentUpdate, MachineLearningFindingCreate, MachineLearningDataPointCreate
from typing import List, Optional

class MachineLearningService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MachineLearningExperiment]:
        return self.db.query(MachineLearningExperiment).filter(MachineLearningExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MachineLearningExperiment]:
        return self.db.query(MachineLearningExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MachineLearningExperimentCreate) -> MachineLearningExperiment:
        db_exp = MachineLearningExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MachineLearningExperimentUpdate) -> Optional[MachineLearningExperiment]:
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

    def create_finding(self, finding_in: MachineLearningFindingCreate) -> MachineLearningFinding:
        db_finding = MachineLearningFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MachineLearningFinding]:
        return self.db.query(MachineLearningFinding).filter(MachineLearningFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MachineLearningDataPointCreate) -> MachineLearningDataPoint:
        db_dp = MachineLearningDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MachineLearningDataPoint]:
        return self.db.query(MachineLearningDataPoint).filter(MachineLearningDataPoint.experiment_id == experiment_id).all()
