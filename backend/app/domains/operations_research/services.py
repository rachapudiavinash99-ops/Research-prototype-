from sqlalchemy.orm import Session
from .models import OperationsResearchExperiment, OperationsResearchFinding, OperationsResearchDataPoint
from .schemas import OperationsResearchExperimentCreate, OperationsResearchExperimentUpdate, OperationsResearchFindingCreate, OperationsResearchDataPointCreate
from typing import List, Optional

class OperationsResearchService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[OperationsResearchExperiment]:
        return self.db.query(OperationsResearchExperiment).filter(OperationsResearchExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[OperationsResearchExperiment]:
        return self.db.query(OperationsResearchExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: OperationsResearchExperimentCreate) -> OperationsResearchExperiment:
        db_exp = OperationsResearchExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: OperationsResearchExperimentUpdate) -> Optional[OperationsResearchExperiment]:
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

    def create_finding(self, finding_in: OperationsResearchFindingCreate) -> OperationsResearchFinding:
        db_finding = OperationsResearchFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[OperationsResearchFinding]:
        return self.db.query(OperationsResearchFinding).filter(OperationsResearchFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: OperationsResearchDataPointCreate) -> OperationsResearchDataPoint:
        db_dp = OperationsResearchDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[OperationsResearchDataPoint]:
        return self.db.query(OperationsResearchDataPoint).filter(OperationsResearchDataPoint.experiment_id == experiment_id).all()
