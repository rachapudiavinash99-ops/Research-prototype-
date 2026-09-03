from sqlalchemy.orm import Session
from .models import ForestryExperiment, ForestryFinding, ForestryDataPoint
from .schemas import ForestryExperimentCreate, ForestryExperimentUpdate, ForestryFindingCreate, ForestryDataPointCreate
from typing import List, Optional

class ForestryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ForestryExperiment]:
        return self.db.query(ForestryExperiment).filter(ForestryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ForestryExperiment]:
        return self.db.query(ForestryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ForestryExperimentCreate) -> ForestryExperiment:
        db_exp = ForestryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ForestryExperimentUpdate) -> Optional[ForestryExperiment]:
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

    def create_finding(self, finding_in: ForestryFindingCreate) -> ForestryFinding:
        db_finding = ForestryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ForestryFinding]:
        return self.db.query(ForestryFinding).filter(ForestryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ForestryDataPointCreate) -> ForestryDataPoint:
        db_dp = ForestryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ForestryDataPoint]:
        return self.db.query(ForestryDataPoint).filter(ForestryDataPoint.experiment_id == experiment_id).all()
