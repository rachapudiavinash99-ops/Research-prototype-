from sqlalchemy.orm import Session
from .models import AlgebraExperiment, AlgebraFinding, AlgebraDataPoint
from .schemas import AlgebraExperimentCreate, AlgebraExperimentUpdate, AlgebraFindingCreate, AlgebraDataPointCreate
from typing import List, Optional

class AlgebraService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AlgebraExperiment]:
        return self.db.query(AlgebraExperiment).filter(AlgebraExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AlgebraExperiment]:
        return self.db.query(AlgebraExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AlgebraExperimentCreate) -> AlgebraExperiment:
        db_exp = AlgebraExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AlgebraExperimentUpdate) -> Optional[AlgebraExperiment]:
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

    def create_finding(self, finding_in: AlgebraFindingCreate) -> AlgebraFinding:
        db_finding = AlgebraFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AlgebraFinding]:
        return self.db.query(AlgebraFinding).filter(AlgebraFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AlgebraDataPointCreate) -> AlgebraDataPoint:
        db_dp = AlgebraDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AlgebraDataPoint]:
        return self.db.query(AlgebraDataPoint).filter(AlgebraDataPoint.experiment_id == experiment_id).all()
