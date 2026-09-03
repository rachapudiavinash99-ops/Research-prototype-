from sqlalchemy.orm import Session
from .models import QuantumMechanicsAdvancedExperiment, QuantumMechanicsAdvancedFinding, QuantumMechanicsAdvancedDataPoint
from .schemas import QuantumMechanicsAdvancedExperimentCreate, QuantumMechanicsAdvancedExperimentUpdate, QuantumMechanicsAdvancedFindingCreate, QuantumMechanicsAdvancedDataPointCreate
from typing import List, Optional

class QuantumMechanicsAdvancedService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[QuantumMechanicsAdvancedExperiment]:
        return self.db.query(QuantumMechanicsAdvancedExperiment).filter(QuantumMechanicsAdvancedExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[QuantumMechanicsAdvancedExperiment]:
        return self.db.query(QuantumMechanicsAdvancedExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: QuantumMechanicsAdvancedExperimentCreate) -> QuantumMechanicsAdvancedExperiment:
        db_exp = QuantumMechanicsAdvancedExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: QuantumMechanicsAdvancedExperimentUpdate) -> Optional[QuantumMechanicsAdvancedExperiment]:
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

    def create_finding(self, finding_in: QuantumMechanicsAdvancedFindingCreate) -> QuantumMechanicsAdvancedFinding:
        db_finding = QuantumMechanicsAdvancedFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[QuantumMechanicsAdvancedFinding]:
        return self.db.query(QuantumMechanicsAdvancedFinding).filter(QuantumMechanicsAdvancedFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: QuantumMechanicsAdvancedDataPointCreate) -> QuantumMechanicsAdvancedDataPoint:
        db_dp = QuantumMechanicsAdvancedDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[QuantumMechanicsAdvancedDataPoint]:
        return self.db.query(QuantumMechanicsAdvancedDataPoint).filter(QuantumMechanicsAdvancedDataPoint.experiment_id == experiment_id).all()
