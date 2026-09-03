from sqlalchemy.orm import Session
from .models import FoodScienceExperiment, FoodScienceFinding, FoodScienceDataPoint
from .schemas import FoodScienceExperimentCreate, FoodScienceExperimentUpdate, FoodScienceFindingCreate, FoodScienceDataPointCreate
from typing import List, Optional

class FoodScienceService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[FoodScienceExperiment]:
        return self.db.query(FoodScienceExperiment).filter(FoodScienceExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[FoodScienceExperiment]:
        return self.db.query(FoodScienceExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: FoodScienceExperimentCreate) -> FoodScienceExperiment:
        db_exp = FoodScienceExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: FoodScienceExperimentUpdate) -> Optional[FoodScienceExperiment]:
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

    def create_finding(self, finding_in: FoodScienceFindingCreate) -> FoodScienceFinding:
        db_finding = FoodScienceFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[FoodScienceFinding]:
        return self.db.query(FoodScienceFinding).filter(FoodScienceFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: FoodScienceDataPointCreate) -> FoodScienceDataPoint:
        db_dp = FoodScienceDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[FoodScienceDataPoint]:
        return self.db.query(FoodScienceDataPoint).filter(FoodScienceDataPoint.experiment_id == experiment_id).all()
