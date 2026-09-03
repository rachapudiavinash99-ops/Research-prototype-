from sqlalchemy.orm import Session
from .models import HydrologyExperiment, HydrologyFinding, HydrologyDataPoint
from .schemas import HydrologyExperimentCreate, HydrologyExperimentUpdate, HydrologyFindingCreate, HydrologyDataPointCreate
from typing import List, Optional

class HydrologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[HydrologyExperiment]:
        return self.db.query(HydrologyExperiment).filter(HydrologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[HydrologyExperiment]:
        return self.db.query(HydrologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: HydrologyExperimentCreate) -> HydrologyExperiment:
        db_exp = HydrologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: HydrologyExperimentUpdate) -> Optional[HydrologyExperiment]:
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

    def create_finding(self, finding_in: HydrologyFindingCreate) -> HydrologyFinding:
        db_finding = HydrologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[HydrologyFinding]:
        return self.db.query(HydrologyFinding).filter(HydrologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: HydrologyDataPointCreate) -> HydrologyDataPoint:
        db_dp = HydrologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[HydrologyDataPoint]:
        return self.db.query(HydrologyDataPoint).filter(HydrologyDataPoint.experiment_id == experiment_id).all()
