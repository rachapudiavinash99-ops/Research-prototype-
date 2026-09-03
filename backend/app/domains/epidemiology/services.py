from sqlalchemy.orm import Session
from .models import EpidemiologyExperiment, EpidemiologyFinding, EpidemiologyDataPoint
from .schemas import EpidemiologyExperimentCreate, EpidemiologyExperimentUpdate, EpidemiologyFindingCreate, EpidemiologyDataPointCreate
from typing import List, Optional

class EpidemiologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[EpidemiologyExperiment]:
        return self.db.query(EpidemiologyExperiment).filter(EpidemiologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[EpidemiologyExperiment]:
        return self.db.query(EpidemiologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: EpidemiologyExperimentCreate) -> EpidemiologyExperiment:
        db_exp = EpidemiologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: EpidemiologyExperimentUpdate) -> Optional[EpidemiologyExperiment]:
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

    def create_finding(self, finding_in: EpidemiologyFindingCreate) -> EpidemiologyFinding:
        db_finding = EpidemiologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[EpidemiologyFinding]:
        return self.db.query(EpidemiologyFinding).filter(EpidemiologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: EpidemiologyDataPointCreate) -> EpidemiologyDataPoint:
        db_dp = EpidemiologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[EpidemiologyDataPoint]:
        return self.db.query(EpidemiologyDataPoint).filter(EpidemiologyDataPoint.experiment_id == experiment_id).all()
