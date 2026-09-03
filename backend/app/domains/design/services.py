from sqlalchemy.orm import Session
from .models import DesignExperiment, DesignFinding, DesignDataPoint
from .schemas import DesignExperimentCreate, DesignExperimentUpdate, DesignFindingCreate, DesignDataPointCreate
from typing import List, Optional

class DesignService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DesignExperiment]:
        return self.db.query(DesignExperiment).filter(DesignExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DesignExperiment]:
        return self.db.query(DesignExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DesignExperimentCreate) -> DesignExperiment:
        db_exp = DesignExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DesignExperimentUpdate) -> Optional[DesignExperiment]:
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

    def create_finding(self, finding_in: DesignFindingCreate) -> DesignFinding:
        db_finding = DesignFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DesignFinding]:
        return self.db.query(DesignFinding).filter(DesignFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DesignDataPointCreate) -> DesignDataPoint:
        db_dp = DesignDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DesignDataPoint]:
        return self.db.query(DesignDataPoint).filter(DesignDataPoint.experiment_id == experiment_id).all()
