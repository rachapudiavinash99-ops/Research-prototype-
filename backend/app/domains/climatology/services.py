from sqlalchemy.orm import Session
from .models import ClimatologyExperiment, ClimatologyFinding, ClimatologyDataPoint
from .schemas import ClimatologyExperimentCreate, ClimatologyExperimentUpdate, ClimatologyFindingCreate, ClimatologyDataPointCreate
from typing import List, Optional

class ClimatologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ClimatologyExperiment]:
        return self.db.query(ClimatologyExperiment).filter(ClimatologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ClimatologyExperiment]:
        return self.db.query(ClimatologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ClimatologyExperimentCreate) -> ClimatologyExperiment:
        db_exp = ClimatologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ClimatologyExperimentUpdate) -> Optional[ClimatologyExperiment]:
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

    def create_finding(self, finding_in: ClimatologyFindingCreate) -> ClimatologyFinding:
        db_finding = ClimatologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ClimatologyFinding]:
        return self.db.query(ClimatologyFinding).filter(ClimatologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ClimatologyDataPointCreate) -> ClimatologyDataPoint:
        db_dp = ClimatologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ClimatologyDataPoint]:
        return self.db.query(ClimatologyDataPoint).filter(ClimatologyDataPoint.experiment_id == experiment_id).all()
