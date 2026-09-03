from sqlalchemy.orm import Session
from .models import MineralogyExperiment, MineralogyFinding, MineralogyDataPoint
from .schemas import MineralogyExperimentCreate, MineralogyExperimentUpdate, MineralogyFindingCreate, MineralogyDataPointCreate
from typing import List, Optional

class MineralogyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MineralogyExperiment]:
        return self.db.query(MineralogyExperiment).filter(MineralogyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MineralogyExperiment]:
        return self.db.query(MineralogyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MineralogyExperimentCreate) -> MineralogyExperiment:
        db_exp = MineralogyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MineralogyExperimentUpdate) -> Optional[MineralogyExperiment]:
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

    def create_finding(self, finding_in: MineralogyFindingCreate) -> MineralogyFinding:
        db_finding = MineralogyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MineralogyFinding]:
        return self.db.query(MineralogyFinding).filter(MineralogyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MineralogyDataPointCreate) -> MineralogyDataPoint:
        db_dp = MineralogyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MineralogyDataPoint]:
        return self.db.query(MineralogyDataPoint).filter(MineralogyDataPoint.experiment_id == experiment_id).all()
