from sqlalchemy.orm import Session
from .models import DiscreteMathematicsExperiment, DiscreteMathematicsFinding, DiscreteMathematicsDataPoint
from .schemas import DiscreteMathematicsExperimentCreate, DiscreteMathematicsExperimentUpdate, DiscreteMathematicsFindingCreate, DiscreteMathematicsDataPointCreate
from typing import List, Optional

class DiscreteMathematicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DiscreteMathematicsExperiment]:
        return self.db.query(DiscreteMathematicsExperiment).filter(DiscreteMathematicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DiscreteMathematicsExperiment]:
        return self.db.query(DiscreteMathematicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DiscreteMathematicsExperimentCreate) -> DiscreteMathematicsExperiment:
        db_exp = DiscreteMathematicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DiscreteMathematicsExperimentUpdate) -> Optional[DiscreteMathematicsExperiment]:
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

    def create_finding(self, finding_in: DiscreteMathematicsFindingCreate) -> DiscreteMathematicsFinding:
        db_finding = DiscreteMathematicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DiscreteMathematicsFinding]:
        return self.db.query(DiscreteMathematicsFinding).filter(DiscreteMathematicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DiscreteMathematicsDataPointCreate) -> DiscreteMathematicsDataPoint:
        db_dp = DiscreteMathematicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DiscreteMathematicsDataPoint]:
        return self.db.query(DiscreteMathematicsDataPoint).filter(DiscreteMathematicsDataPoint.experiment_id == experiment_id).all()
