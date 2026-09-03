from sqlalchemy.orm import Session
from .models import KinesiologyExperiment, KinesiologyFinding, KinesiologyDataPoint
from .schemas import KinesiologyExperimentCreate, KinesiologyExperimentUpdate, KinesiologyFindingCreate, KinesiologyDataPointCreate
from typing import List, Optional

class KinesiologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[KinesiologyExperiment]:
        return self.db.query(KinesiologyExperiment).filter(KinesiologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[KinesiologyExperiment]:
        return self.db.query(KinesiologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: KinesiologyExperimentCreate) -> KinesiologyExperiment:
        db_exp = KinesiologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: KinesiologyExperimentUpdate) -> Optional[KinesiologyExperiment]:
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

    def create_finding(self, finding_in: KinesiologyFindingCreate) -> KinesiologyFinding:
        db_finding = KinesiologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[KinesiologyFinding]:
        return self.db.query(KinesiologyFinding).filter(KinesiologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: KinesiologyDataPointCreate) -> KinesiologyDataPoint:
        db_dp = KinesiologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[KinesiologyDataPoint]:
        return self.db.query(KinesiologyDataPoint).filter(KinesiologyDataPoint.experiment_id == experiment_id).all()
