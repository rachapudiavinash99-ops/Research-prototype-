from sqlalchemy.orm import Session
from .models import DifferentialEquationsExperiment, DifferentialEquationsFinding, DifferentialEquationsDataPoint
from .schemas import DifferentialEquationsExperimentCreate, DifferentialEquationsExperimentUpdate, DifferentialEquationsFindingCreate, DifferentialEquationsDataPointCreate
from typing import List, Optional

class DifferentialEquationsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DifferentialEquationsExperiment]:
        return self.db.query(DifferentialEquationsExperiment).filter(DifferentialEquationsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DifferentialEquationsExperiment]:
        return self.db.query(DifferentialEquationsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DifferentialEquationsExperimentCreate) -> DifferentialEquationsExperiment:
        db_exp = DifferentialEquationsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DifferentialEquationsExperimentUpdate) -> Optional[DifferentialEquationsExperiment]:
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

    def create_finding(self, finding_in: DifferentialEquationsFindingCreate) -> DifferentialEquationsFinding:
        db_finding = DifferentialEquationsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DifferentialEquationsFinding]:
        return self.db.query(DifferentialEquationsFinding).filter(DifferentialEquationsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DifferentialEquationsDataPointCreate) -> DifferentialEquationsDataPoint:
        db_dp = DifferentialEquationsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DifferentialEquationsDataPoint]:
        return self.db.query(DifferentialEquationsDataPoint).filter(DifferentialEquationsDataPoint.experiment_id == experiment_id).all()
