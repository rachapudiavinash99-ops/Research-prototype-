from sqlalchemy.orm import Session
from .models import ProteomicsExperiment, ProteomicsFinding, ProteomicsDataPoint
from .schemas import ProteomicsExperimentCreate, ProteomicsExperimentUpdate, ProteomicsFindingCreate, ProteomicsDataPointCreate
from typing import List, Optional

class ProteomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ProteomicsExperiment]:
        return self.db.query(ProteomicsExperiment).filter(ProteomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ProteomicsExperiment]:
        return self.db.query(ProteomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ProteomicsExperimentCreate) -> ProteomicsExperiment:
        db_exp = ProteomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ProteomicsExperimentUpdate) -> Optional[ProteomicsExperiment]:
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

    def create_finding(self, finding_in: ProteomicsFindingCreate) -> ProteomicsFinding:
        db_finding = ProteomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ProteomicsFinding]:
        return self.db.query(ProteomicsFinding).filter(ProteomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ProteomicsDataPointCreate) -> ProteomicsDataPoint:
        db_dp = ProteomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ProteomicsDataPoint]:
        return self.db.query(ProteomicsDataPoint).filter(ProteomicsDataPoint.experiment_id == experiment_id).all()
