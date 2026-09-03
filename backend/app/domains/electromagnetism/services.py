from sqlalchemy.orm import Session
from .models import ElectromagnetismExperiment, ElectromagnetismFinding, ElectromagnetismDataPoint
from .schemas import ElectromagnetismExperimentCreate, ElectromagnetismExperimentUpdate, ElectromagnetismFindingCreate, ElectromagnetismDataPointCreate
from typing import List, Optional

class ElectromagnetismService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ElectromagnetismExperiment]:
        return self.db.query(ElectromagnetismExperiment).filter(ElectromagnetismExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ElectromagnetismExperiment]:
        return self.db.query(ElectromagnetismExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ElectromagnetismExperimentCreate) -> ElectromagnetismExperiment:
        db_exp = ElectromagnetismExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ElectromagnetismExperimentUpdate) -> Optional[ElectromagnetismExperiment]:
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

    def create_finding(self, finding_in: ElectromagnetismFindingCreate) -> ElectromagnetismFinding:
        db_finding = ElectromagnetismFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ElectromagnetismFinding]:
        return self.db.query(ElectromagnetismFinding).filter(ElectromagnetismFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ElectromagnetismDataPointCreate) -> ElectromagnetismDataPoint:
        db_dp = ElectromagnetismDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ElectromagnetismDataPoint]:
        return self.db.query(ElectromagnetismDataPoint).filter(ElectromagnetismDataPoint.experiment_id == experiment_id).all()
