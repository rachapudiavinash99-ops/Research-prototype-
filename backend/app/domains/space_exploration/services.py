from sqlalchemy.orm import Session
from .models import SpaceExplorationExperiment, SpaceExplorationFinding, SpaceExplorationDataPoint
from .schemas import SpaceExplorationExperimentCreate, SpaceExplorationExperimentUpdate, SpaceExplorationFindingCreate, SpaceExplorationDataPointCreate
from typing import List, Optional

class SpaceExplorationService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SpaceExplorationExperiment]:
        return self.db.query(SpaceExplorationExperiment).filter(SpaceExplorationExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SpaceExplorationExperiment]:
        return self.db.query(SpaceExplorationExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SpaceExplorationExperimentCreate) -> SpaceExplorationExperiment:
        db_exp = SpaceExplorationExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SpaceExplorationExperimentUpdate) -> Optional[SpaceExplorationExperiment]:
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

    def create_finding(self, finding_in: SpaceExplorationFindingCreate) -> SpaceExplorationFinding:
        db_finding = SpaceExplorationFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SpaceExplorationFinding]:
        return self.db.query(SpaceExplorationFinding).filter(SpaceExplorationFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SpaceExplorationDataPointCreate) -> SpaceExplorationDataPoint:
        db_dp = SpaceExplorationDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SpaceExplorationDataPoint]:
        return self.db.query(SpaceExplorationDataPoint).filter(SpaceExplorationDataPoint.experiment_id == experiment_id).all()
