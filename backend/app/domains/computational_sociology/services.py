from sqlalchemy.orm import Session
from .models import ComputationalSociologyExperiment, ComputationalSociologyFinding, ComputationalSociologyDataPoint
from .schemas import ComputationalSociologyExperimentCreate, ComputationalSociologyExperimentUpdate, ComputationalSociologyFindingCreate, ComputationalSociologyDataPointCreate
from typing import List, Optional

class ComputationalSociologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ComputationalSociologyExperiment]:
        return self.db.query(ComputationalSociologyExperiment).filter(ComputationalSociologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ComputationalSociologyExperiment]:
        return self.db.query(ComputationalSociologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ComputationalSociologyExperimentCreate) -> ComputationalSociologyExperiment:
        db_exp = ComputationalSociologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ComputationalSociologyExperimentUpdate) -> Optional[ComputationalSociologyExperiment]:
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

    def create_finding(self, finding_in: ComputationalSociologyFindingCreate) -> ComputationalSociologyFinding:
        db_finding = ComputationalSociologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ComputationalSociologyFinding]:
        return self.db.query(ComputationalSociologyFinding).filter(ComputationalSociologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ComputationalSociologyDataPointCreate) -> ComputationalSociologyDataPoint:
        db_dp = ComputationalSociologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ComputationalSociologyDataPoint]:
        return self.db.query(ComputationalSociologyDataPoint).filter(ComputationalSociologyDataPoint.experiment_id == experiment_id).all()
