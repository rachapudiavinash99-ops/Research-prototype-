from sqlalchemy.orm import Session
from .models import SyntheticBiologyExperiment, SyntheticBiologyFinding, SyntheticBiologyDataPoint
from .schemas import SyntheticBiologyExperimentCreate, SyntheticBiologyExperimentUpdate, SyntheticBiologyFindingCreate, SyntheticBiologyDataPointCreate
from typing import List, Optional

class SyntheticBiologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SyntheticBiologyExperiment]:
        return self.db.query(SyntheticBiologyExperiment).filter(SyntheticBiologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SyntheticBiologyExperiment]:
        return self.db.query(SyntheticBiologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SyntheticBiologyExperimentCreate) -> SyntheticBiologyExperiment:
        db_exp = SyntheticBiologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SyntheticBiologyExperimentUpdate) -> Optional[SyntheticBiologyExperiment]:
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

    def create_finding(self, finding_in: SyntheticBiologyFindingCreate) -> SyntheticBiologyFinding:
        db_finding = SyntheticBiologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SyntheticBiologyFinding]:
        return self.db.query(SyntheticBiologyFinding).filter(SyntheticBiologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SyntheticBiologyDataPointCreate) -> SyntheticBiologyDataPoint:
        db_dp = SyntheticBiologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SyntheticBiologyDataPoint]:
        return self.db.query(SyntheticBiologyDataPoint).filter(SyntheticBiologyDataPoint.experiment_id == experiment_id).all()
