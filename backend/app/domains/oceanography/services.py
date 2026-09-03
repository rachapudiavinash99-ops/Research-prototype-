from sqlalchemy.orm import Session
from .models import OceanographyExperiment, OceanographyFinding, OceanographyDataPoint
from .schemas import OceanographyExperimentCreate, OceanographyExperimentUpdate, OceanographyFindingCreate, OceanographyDataPointCreate
from typing import List, Optional

class OceanographyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[OceanographyExperiment]:
        return self.db.query(OceanographyExperiment).filter(OceanographyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[OceanographyExperiment]:
        return self.db.query(OceanographyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: OceanographyExperimentCreate) -> OceanographyExperiment:
        db_exp = OceanographyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: OceanographyExperimentUpdate) -> Optional[OceanographyExperiment]:
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

    def create_finding(self, finding_in: OceanographyFindingCreate) -> OceanographyFinding:
        db_finding = OceanographyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[OceanographyFinding]:
        return self.db.query(OceanographyFinding).filter(OceanographyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: OceanographyDataPointCreate) -> OceanographyDataPoint:
        db_dp = OceanographyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[OceanographyDataPoint]:
        return self.db.query(OceanographyDataPoint).filter(OceanographyDataPoint.experiment_id == experiment_id).all()
