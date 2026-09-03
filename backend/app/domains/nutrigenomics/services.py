from sqlalchemy.orm import Session
from .models import NutrigenomicsExperiment, NutrigenomicsFinding, NutrigenomicsDataPoint
from .schemas import NutrigenomicsExperimentCreate, NutrigenomicsExperimentUpdate, NutrigenomicsFindingCreate, NutrigenomicsDataPointCreate
from typing import List, Optional

class NutrigenomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[NutrigenomicsExperiment]:
        return self.db.query(NutrigenomicsExperiment).filter(NutrigenomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[NutrigenomicsExperiment]:
        return self.db.query(NutrigenomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: NutrigenomicsExperimentCreate) -> NutrigenomicsExperiment:
        db_exp = NutrigenomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: NutrigenomicsExperimentUpdate) -> Optional[NutrigenomicsExperiment]:
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

    def create_finding(self, finding_in: NutrigenomicsFindingCreate) -> NutrigenomicsFinding:
        db_finding = NutrigenomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[NutrigenomicsFinding]:
        return self.db.query(NutrigenomicsFinding).filter(NutrigenomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: NutrigenomicsDataPointCreate) -> NutrigenomicsDataPoint:
        db_dp = NutrigenomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[NutrigenomicsDataPoint]:
        return self.db.query(NutrigenomicsDataPoint).filter(NutrigenomicsDataPoint.experiment_id == experiment_id).all()
