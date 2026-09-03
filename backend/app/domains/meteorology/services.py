from sqlalchemy.orm import Session
from .models import MeteorologyExperiment, MeteorologyFinding, MeteorologyDataPoint
from .schemas import MeteorologyExperimentCreate, MeteorologyExperimentUpdate, MeteorologyFindingCreate, MeteorologyDataPointCreate
from typing import List, Optional

class MeteorologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MeteorologyExperiment]:
        return self.db.query(MeteorologyExperiment).filter(MeteorologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MeteorologyExperiment]:
        return self.db.query(MeteorologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MeteorologyExperimentCreate) -> MeteorologyExperiment:
        db_exp = MeteorologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MeteorologyExperimentUpdate) -> Optional[MeteorologyExperiment]:
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

    def create_finding(self, finding_in: MeteorologyFindingCreate) -> MeteorologyFinding:
        db_finding = MeteorologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MeteorologyFinding]:
        return self.db.query(MeteorologyFinding).filter(MeteorologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MeteorologyDataPointCreate) -> MeteorologyDataPoint:
        db_dp = MeteorologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MeteorologyDataPoint]:
        return self.db.query(MeteorologyDataPoint).filter(MeteorologyDataPoint.experiment_id == experiment_id).all()
