from sqlalchemy.orm import Session
from .models import UrbanPlanningExperiment, UrbanPlanningFinding, UrbanPlanningDataPoint
from .schemas import UrbanPlanningExperimentCreate, UrbanPlanningExperimentUpdate, UrbanPlanningFindingCreate, UrbanPlanningDataPointCreate
from typing import List, Optional

class UrbanPlanningService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[UrbanPlanningExperiment]:
        return self.db.query(UrbanPlanningExperiment).filter(UrbanPlanningExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[UrbanPlanningExperiment]:
        return self.db.query(UrbanPlanningExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: UrbanPlanningExperimentCreate) -> UrbanPlanningExperiment:
        db_exp = UrbanPlanningExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: UrbanPlanningExperimentUpdate) -> Optional[UrbanPlanningExperiment]:
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

    def create_finding(self, finding_in: UrbanPlanningFindingCreate) -> UrbanPlanningFinding:
        db_finding = UrbanPlanningFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[UrbanPlanningFinding]:
        return self.db.query(UrbanPlanningFinding).filter(UrbanPlanningFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: UrbanPlanningDataPointCreate) -> UrbanPlanningDataPoint:
        db_dp = UrbanPlanningDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[UrbanPlanningDataPoint]:
        return self.db.query(UrbanPlanningDataPoint).filter(UrbanPlanningDataPoint.experiment_id == experiment_id).all()
