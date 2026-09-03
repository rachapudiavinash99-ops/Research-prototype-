from sqlalchemy.orm import Session
from .models import AquacultureExperiment, AquacultureFinding, AquacultureDataPoint
from .schemas import AquacultureExperimentCreate, AquacultureExperimentUpdate, AquacultureFindingCreate, AquacultureDataPointCreate
from typing import List, Optional

class AquacultureService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AquacultureExperiment]:
        return self.db.query(AquacultureExperiment).filter(AquacultureExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AquacultureExperiment]:
        return self.db.query(AquacultureExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AquacultureExperimentCreate) -> AquacultureExperiment:
        db_exp = AquacultureExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AquacultureExperimentUpdate) -> Optional[AquacultureExperiment]:
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

    def create_finding(self, finding_in: AquacultureFindingCreate) -> AquacultureFinding:
        db_finding = AquacultureFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AquacultureFinding]:
        return self.db.query(AquacultureFinding).filter(AquacultureFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AquacultureDataPointCreate) -> AquacultureDataPoint:
        db_dp = AquacultureDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AquacultureDataPoint]:
        return self.db.query(AquacultureDataPoint).filter(AquacultureDataPoint.experiment_id == experiment_id).all()
