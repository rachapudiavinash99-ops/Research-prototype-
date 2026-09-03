from sqlalchemy.orm import Session
from .models import NetworkingExperiment, NetworkingFinding, NetworkingDataPoint
from .schemas import NetworkingExperimentCreate, NetworkingExperimentUpdate, NetworkingFindingCreate, NetworkingDataPointCreate
from typing import List, Optional

class NetworkingService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[NetworkingExperiment]:
        return self.db.query(NetworkingExperiment).filter(NetworkingExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[NetworkingExperiment]:
        return self.db.query(NetworkingExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: NetworkingExperimentCreate) -> NetworkingExperiment:
        db_exp = NetworkingExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: NetworkingExperimentUpdate) -> Optional[NetworkingExperiment]:
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

    def create_finding(self, finding_in: NetworkingFindingCreate) -> NetworkingFinding:
        db_finding = NetworkingFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[NetworkingFinding]:
        return self.db.query(NetworkingFinding).filter(NetworkingFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: NetworkingDataPointCreate) -> NetworkingDataPoint:
        db_dp = NetworkingDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[NetworkingDataPoint]:
        return self.db.query(NetworkingDataPoint).filter(NetworkingDataPoint.experiment_id == experiment_id).all()
