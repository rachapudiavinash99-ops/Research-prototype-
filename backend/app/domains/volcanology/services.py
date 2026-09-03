from sqlalchemy.orm import Session
from .models import VolcanologyExperiment, VolcanologyFinding, VolcanologyDataPoint
from .schemas import VolcanologyExperimentCreate, VolcanologyExperimentUpdate, VolcanologyFindingCreate, VolcanologyDataPointCreate
from typing import List, Optional

class VolcanologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[VolcanologyExperiment]:
        return self.db.query(VolcanologyExperiment).filter(VolcanologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[VolcanologyExperiment]:
        return self.db.query(VolcanologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: VolcanologyExperimentCreate) -> VolcanologyExperiment:
        db_exp = VolcanologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: VolcanologyExperimentUpdate) -> Optional[VolcanologyExperiment]:
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

    def create_finding(self, finding_in: VolcanologyFindingCreate) -> VolcanologyFinding:
        db_finding = VolcanologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[VolcanologyFinding]:
        return self.db.query(VolcanologyFinding).filter(VolcanologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: VolcanologyDataPointCreate) -> VolcanologyDataPoint:
        db_dp = VolcanologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[VolcanologyDataPoint]:
        return self.db.query(VolcanologyDataPoint).filter(VolcanologyDataPoint.experiment_id == experiment_id).all()
