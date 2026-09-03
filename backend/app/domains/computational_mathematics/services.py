from sqlalchemy.orm import Session
from .models import ComputationalMathematicsExperiment, ComputationalMathematicsFinding, ComputationalMathematicsDataPoint
from .schemas import ComputationalMathematicsExperimentCreate, ComputationalMathematicsExperimentUpdate, ComputationalMathematicsFindingCreate, ComputationalMathematicsDataPointCreate
from typing import List, Optional

class ComputationalMathematicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ComputationalMathematicsExperiment]:
        return self.db.query(ComputationalMathematicsExperiment).filter(ComputationalMathematicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ComputationalMathematicsExperiment]:
        return self.db.query(ComputationalMathematicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ComputationalMathematicsExperimentCreate) -> ComputationalMathematicsExperiment:
        db_exp = ComputationalMathematicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ComputationalMathematicsExperimentUpdate) -> Optional[ComputationalMathematicsExperiment]:
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

    def create_finding(self, finding_in: ComputationalMathematicsFindingCreate) -> ComputationalMathematicsFinding:
        db_finding = ComputationalMathematicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ComputationalMathematicsFinding]:
        return self.db.query(ComputationalMathematicsFinding).filter(ComputationalMathematicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ComputationalMathematicsDataPointCreate) -> ComputationalMathematicsDataPoint:
        db_dp = ComputationalMathematicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ComputationalMathematicsDataPoint]:
        return self.db.query(ComputationalMathematicsDataPoint).filter(ComputationalMathematicsDataPoint.experiment_id == experiment_id).all()
