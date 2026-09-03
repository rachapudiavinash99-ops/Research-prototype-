from sqlalchemy.orm import Session
from .models import CommunicationStudiesExperiment, CommunicationStudiesFinding, CommunicationStudiesDataPoint
from .schemas import CommunicationStudiesExperimentCreate, CommunicationStudiesExperimentUpdate, CommunicationStudiesFindingCreate, CommunicationStudiesDataPointCreate
from typing import List, Optional

class CommunicationStudiesService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CommunicationStudiesExperiment]:
        return self.db.query(CommunicationStudiesExperiment).filter(CommunicationStudiesExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CommunicationStudiesExperiment]:
        return self.db.query(CommunicationStudiesExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CommunicationStudiesExperimentCreate) -> CommunicationStudiesExperiment:
        db_exp = CommunicationStudiesExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CommunicationStudiesExperimentUpdate) -> Optional[CommunicationStudiesExperiment]:
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

    def create_finding(self, finding_in: CommunicationStudiesFindingCreate) -> CommunicationStudiesFinding:
        db_finding = CommunicationStudiesFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CommunicationStudiesFinding]:
        return self.db.query(CommunicationStudiesFinding).filter(CommunicationStudiesFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CommunicationStudiesDataPointCreate) -> CommunicationStudiesDataPoint:
        db_dp = CommunicationStudiesDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CommunicationStudiesDataPoint]:
        return self.db.query(CommunicationStudiesDataPoint).filter(CommunicationStudiesDataPoint.experiment_id == experiment_id).all()
