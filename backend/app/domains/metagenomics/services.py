from sqlalchemy.orm import Session
from .models import MetagenomicsExperiment, MetagenomicsFinding, MetagenomicsDataPoint
from .schemas import MetagenomicsExperimentCreate, MetagenomicsExperimentUpdate, MetagenomicsFindingCreate, MetagenomicsDataPointCreate
from typing import List, Optional

class MetagenomicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MetagenomicsExperiment]:
        return self.db.query(MetagenomicsExperiment).filter(MetagenomicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MetagenomicsExperiment]:
        return self.db.query(MetagenomicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MetagenomicsExperimentCreate) -> MetagenomicsExperiment:
        db_exp = MetagenomicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MetagenomicsExperimentUpdate) -> Optional[MetagenomicsExperiment]:
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

    def create_finding(self, finding_in: MetagenomicsFindingCreate) -> MetagenomicsFinding:
        db_finding = MetagenomicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MetagenomicsFinding]:
        return self.db.query(MetagenomicsFinding).filter(MetagenomicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MetagenomicsDataPointCreate) -> MetagenomicsDataPoint:
        db_dp = MetagenomicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MetagenomicsDataPoint]:
        return self.db.query(MetagenomicsDataPoint).filter(MetagenomicsDataPoint.experiment_id == experiment_id).all()
