from sqlalchemy.orm import Session
from .models import DigitalHumanitiesExperiment, DigitalHumanitiesFinding, DigitalHumanitiesDataPoint
from .schemas import DigitalHumanitiesExperimentCreate, DigitalHumanitiesExperimentUpdate, DigitalHumanitiesFindingCreate, DigitalHumanitiesDataPointCreate
from typing import List, Optional

class DigitalHumanitiesService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DigitalHumanitiesExperiment]:
        return self.db.query(DigitalHumanitiesExperiment).filter(DigitalHumanitiesExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DigitalHumanitiesExperiment]:
        return self.db.query(DigitalHumanitiesExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DigitalHumanitiesExperimentCreate) -> DigitalHumanitiesExperiment:
        db_exp = DigitalHumanitiesExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DigitalHumanitiesExperimentUpdate) -> Optional[DigitalHumanitiesExperiment]:
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

    def create_finding(self, finding_in: DigitalHumanitiesFindingCreate) -> DigitalHumanitiesFinding:
        db_finding = DigitalHumanitiesFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DigitalHumanitiesFinding]:
        return self.db.query(DigitalHumanitiesFinding).filter(DigitalHumanitiesFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DigitalHumanitiesDataPointCreate) -> DigitalHumanitiesDataPoint:
        db_dp = DigitalHumanitiesDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DigitalHumanitiesDataPoint]:
        return self.db.query(DigitalHumanitiesDataPoint).filter(DigitalHumanitiesDataPoint.experiment_id == experiment_id).all()
