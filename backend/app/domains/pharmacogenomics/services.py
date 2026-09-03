from sqlalchemy.orm import Session
from .models import PharmacogenomicsExperiment, PharmacogenomicsFinding, PharmacogenomicsDataPoint
from .schemas import PharmacogenomicsExperimentCreate, PharmacogenomicsExperimentUpdate, PharmacogenomicsFindingCreate, PharmacogenomicsDataPointCreate
from typing import List, Optional

class PharmacogenomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[PharmacogenomicsExperiment]:
        return self.db.query(PharmacogenomicsExperiment).filter(PharmacogenomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[PharmacogenomicsExperiment]:
        return self.db.query(PharmacogenomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: PharmacogenomicsExperimentCreate) -> PharmacogenomicsExperiment:
        db_exp = PharmacogenomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: PharmacogenomicsExperimentUpdate) -> Optional[PharmacogenomicsExperiment]:
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

    def create_finding(self, finding_in: PharmacogenomicsFindingCreate) -> PharmacogenomicsFinding:
        db_finding = PharmacogenomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[PharmacogenomicsFinding]:
        return self.db.query(PharmacogenomicsFinding).filter(PharmacogenomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: PharmacogenomicsDataPointCreate) -> PharmacogenomicsDataPoint:
        db_dp = PharmacogenomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[PharmacogenomicsDataPoint]:
        return self.db.query(PharmacogenomicsDataPoint).filter(PharmacogenomicsDataPoint.experiment_id == experiment_id).all()
