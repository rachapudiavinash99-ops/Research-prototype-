from sqlalchemy.orm import Session
from .models import AiExperiment, AiFinding, AiDataPoint
from .schemas import AiExperimentCreate, AiExperimentUpdate, AiFindingCreate, AiDataPointCreate
from typing import List, Optional

class AiService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AiExperiment]:
        return self.db.query(AiExperiment).filter(AiExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AiExperiment]:
        return self.db.query(AiExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AiExperimentCreate) -> AiExperiment:
        db_exp = AiExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AiExperimentUpdate) -> Optional[AiExperiment]:
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

    def create_finding(self, finding_in: AiFindingCreate) -> AiFinding:
        db_finding = AiFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AiFinding]:
        return self.db.query(AiFinding).filter(AiFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AiDataPointCreate) -> AiDataPoint:
        db_dp = AiDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AiDataPoint]:
        return self.db.query(AiDataPoint).filter(AiDataPoint.experiment_id == experiment_id).all()
