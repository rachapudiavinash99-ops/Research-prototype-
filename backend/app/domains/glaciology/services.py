from sqlalchemy.orm import Session
from .models import GlaciologyExperiment, GlaciologyFinding, GlaciologyDataPoint
from .schemas import GlaciologyExperimentCreate, GlaciologyExperimentUpdate, GlaciologyFindingCreate, GlaciologyDataPointCreate
from typing import List, Optional

class GlaciologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[GlaciologyExperiment]:
        return self.db.query(GlaciologyExperiment).filter(GlaciologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[GlaciologyExperiment]:
        return self.db.query(GlaciologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: GlaciologyExperimentCreate) -> GlaciologyExperiment:
        db_exp = GlaciologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: GlaciologyExperimentUpdate) -> Optional[GlaciologyExperiment]:
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

    def create_finding(self, finding_in: GlaciologyFindingCreate) -> GlaciologyFinding:
        db_finding = GlaciologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[GlaciologyFinding]:
        return self.db.query(GlaciologyFinding).filter(GlaciologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: GlaciologyDataPointCreate) -> GlaciologyDataPoint:
        db_dp = GlaciologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[GlaciologyDataPoint]:
        return self.db.query(GlaciologyDataPoint).filter(GlaciologyDataPoint.experiment_id == experiment_id).all()
