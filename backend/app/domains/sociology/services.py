from sqlalchemy.orm import Session
from .models import SociologyExperiment, SociologyFinding, SociologyDataPoint
from .schemas import SociologyExperimentCreate, SociologyExperimentUpdate, SociologyFindingCreate, SociologyDataPointCreate
from typing import List, Optional

class SociologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SociologyExperiment]:
        return self.db.query(SociologyExperiment).filter(SociologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SociologyExperiment]:
        return self.db.query(SociologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SociologyExperimentCreate) -> SociologyExperiment:
        db_exp = SociologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SociologyExperimentUpdate) -> Optional[SociologyExperiment]:
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

    def create_finding(self, finding_in: SociologyFindingCreate) -> SociologyFinding:
        db_finding = SociologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SociologyFinding]:
        return self.db.query(SociologyFinding).filter(SociologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SociologyDataPointCreate) -> SociologyDataPoint:
        db_dp = SociologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SociologyDataPoint]:
        return self.db.query(SociologyDataPoint).filter(SociologyDataPoint.experiment_id == experiment_id).all()
