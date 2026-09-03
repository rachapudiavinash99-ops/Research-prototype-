from sqlalchemy.orm import Session
from .models import SystemsBiologyExperiment, SystemsBiologyFinding, SystemsBiologyDataPoint
from .schemas import SystemsBiologyExperimentCreate, SystemsBiologyExperimentUpdate, SystemsBiologyFindingCreate, SystemsBiologyDataPointCreate
from typing import List, Optional

class SystemsBiologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SystemsBiologyExperiment]:
        return self.db.query(SystemsBiologyExperiment).filter(SystemsBiologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SystemsBiologyExperiment]:
        return self.db.query(SystemsBiologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SystemsBiologyExperimentCreate) -> SystemsBiologyExperiment:
        db_exp = SystemsBiologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SystemsBiologyExperimentUpdate) -> Optional[SystemsBiologyExperiment]:
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

    def create_finding(self, finding_in: SystemsBiologyFindingCreate) -> SystemsBiologyFinding:
        db_finding = SystemsBiologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SystemsBiologyFinding]:
        return self.db.query(SystemsBiologyFinding).filter(SystemsBiologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SystemsBiologyDataPointCreate) -> SystemsBiologyDataPoint:
        db_dp = SystemsBiologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SystemsBiologyDataPoint]:
        return self.db.query(SystemsBiologyDataPoint).filter(SystemsBiologyDataPoint.experiment_id == experiment_id).all()
