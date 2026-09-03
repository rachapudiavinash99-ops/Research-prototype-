from sqlalchemy.orm import Session
from .models import BioinformaticsAdvancedExperiment, BioinformaticsAdvancedFinding, BioinformaticsAdvancedDataPoint
from .schemas import BioinformaticsAdvancedExperimentCreate, BioinformaticsAdvancedExperimentUpdate, BioinformaticsAdvancedFindingCreate, BioinformaticsAdvancedDataPointCreate
from typing import List, Optional

class BioinformaticsAdvancedService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[BioinformaticsAdvancedExperiment]:
        return self.db.query(BioinformaticsAdvancedExperiment).filter(BioinformaticsAdvancedExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[BioinformaticsAdvancedExperiment]:
        return self.db.query(BioinformaticsAdvancedExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: BioinformaticsAdvancedExperimentCreate) -> BioinformaticsAdvancedExperiment:
        db_exp = BioinformaticsAdvancedExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: BioinformaticsAdvancedExperimentUpdate) -> Optional[BioinformaticsAdvancedExperiment]:
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

    def create_finding(self, finding_in: BioinformaticsAdvancedFindingCreate) -> BioinformaticsAdvancedFinding:
        db_finding = BioinformaticsAdvancedFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[BioinformaticsAdvancedFinding]:
        return self.db.query(BioinformaticsAdvancedFinding).filter(BioinformaticsAdvancedFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: BioinformaticsAdvancedDataPointCreate) -> BioinformaticsAdvancedDataPoint:
        db_dp = BioinformaticsAdvancedDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[BioinformaticsAdvancedDataPoint]:
        return self.db.query(BioinformaticsAdvancedDataPoint).filter(BioinformaticsAdvancedDataPoint.experiment_id == experiment_id).all()
