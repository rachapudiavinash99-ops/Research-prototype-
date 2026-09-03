from sqlalchemy.orm import Session
from .models import ZoologyExperiment, ZoologyFinding, ZoologyDataPoint
from .schemas import ZoologyExperimentCreate, ZoologyExperimentUpdate, ZoologyFindingCreate, ZoologyDataPointCreate
from typing import List, Optional

class ZoologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ZoologyExperiment]:
        return self.db.query(ZoologyExperiment).filter(ZoologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ZoologyExperiment]:
        return self.db.query(ZoologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ZoologyExperimentCreate) -> ZoologyExperiment:
        db_exp = ZoologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ZoologyExperimentUpdate) -> Optional[ZoologyExperiment]:
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

    def create_finding(self, finding_in: ZoologyFindingCreate) -> ZoologyFinding:
        db_finding = ZoologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ZoologyFinding]:
        return self.db.query(ZoologyFinding).filter(ZoologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ZoologyDataPointCreate) -> ZoologyDataPoint:
        db_dp = ZoologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ZoologyDataPoint]:
        return self.db.query(ZoologyDataPoint).filter(ZoologyDataPoint.experiment_id == experiment_id).all()
