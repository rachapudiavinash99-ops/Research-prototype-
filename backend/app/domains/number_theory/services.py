from sqlalchemy.orm import Session
from .models import NumberTheoryExperiment, NumberTheoryFinding, NumberTheoryDataPoint
from .schemas import NumberTheoryExperimentCreate, NumberTheoryExperimentUpdate, NumberTheoryFindingCreate, NumberTheoryDataPointCreate
from typing import List, Optional

class NumberTheoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[NumberTheoryExperiment]:
        return self.db.query(NumberTheoryExperiment).filter(NumberTheoryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[NumberTheoryExperiment]:
        return self.db.query(NumberTheoryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: NumberTheoryExperimentCreate) -> NumberTheoryExperiment:
        db_exp = NumberTheoryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: NumberTheoryExperimentUpdate) -> Optional[NumberTheoryExperiment]:
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

    def create_finding(self, finding_in: NumberTheoryFindingCreate) -> NumberTheoryFinding:
        db_finding = NumberTheoryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[NumberTheoryFinding]:
        return self.db.query(NumberTheoryFinding).filter(NumberTheoryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: NumberTheoryDataPointCreate) -> NumberTheoryDataPoint:
        db_dp = NumberTheoryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[NumberTheoryDataPoint]:
        return self.db.query(NumberTheoryDataPoint).filter(NumberTheoryDataPoint.experiment_id == experiment_id).all()
