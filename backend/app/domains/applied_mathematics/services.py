from sqlalchemy.orm import Session
from .models import AppliedMathematicsExperiment, AppliedMathematicsFinding, AppliedMathematicsDataPoint
from .schemas import AppliedMathematicsExperimentCreate, AppliedMathematicsExperimentUpdate, AppliedMathematicsFindingCreate, AppliedMathematicsDataPointCreate
from typing import List, Optional

class AppliedMathematicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AppliedMathematicsExperiment]:
        return self.db.query(AppliedMathematicsExperiment).filter(AppliedMathematicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AppliedMathematicsExperiment]:
        return self.db.query(AppliedMathematicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AppliedMathematicsExperimentCreate) -> AppliedMathematicsExperiment:
        db_exp = AppliedMathematicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AppliedMathematicsExperimentUpdate) -> Optional[AppliedMathematicsExperiment]:
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

    def create_finding(self, finding_in: AppliedMathematicsFindingCreate) -> AppliedMathematicsFinding:
        db_finding = AppliedMathematicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AppliedMathematicsFinding]:
        return self.db.query(AppliedMathematicsFinding).filter(AppliedMathematicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AppliedMathematicsDataPointCreate) -> AppliedMathematicsDataPoint:
        db_dp = AppliedMathematicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AppliedMathematicsDataPoint]:
        return self.db.query(AppliedMathematicsDataPoint).filter(AppliedMathematicsDataPoint.experiment_id == experiment_id).all()
