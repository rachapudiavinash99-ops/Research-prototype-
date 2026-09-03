from sqlalchemy.orm import Session
from .models import EdgeComputingExperiment, EdgeComputingFinding, EdgeComputingDataPoint
from .schemas import EdgeComputingExperimentCreate, EdgeComputingExperimentUpdate, EdgeComputingFindingCreate, EdgeComputingDataPointCreate
from typing import List, Optional

class EdgeComputingService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[EdgeComputingExperiment]:
        return self.db.query(EdgeComputingExperiment).filter(EdgeComputingExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[EdgeComputingExperiment]:
        return self.db.query(EdgeComputingExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: EdgeComputingExperimentCreate) -> EdgeComputingExperiment:
        db_exp = EdgeComputingExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: EdgeComputingExperimentUpdate) -> Optional[EdgeComputingExperiment]:
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

    def create_finding(self, finding_in: EdgeComputingFindingCreate) -> EdgeComputingFinding:
        db_finding = EdgeComputingFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[EdgeComputingFinding]:
        return self.db.query(EdgeComputingFinding).filter(EdgeComputingFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: EdgeComputingDataPointCreate) -> EdgeComputingDataPoint:
        db_dp = EdgeComputingDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[EdgeComputingDataPoint]:
        return self.db.query(EdgeComputingDataPoint).filter(EdgeComputingDataPoint.experiment_id == experiment_id).all()
