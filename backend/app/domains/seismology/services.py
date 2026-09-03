from sqlalchemy.orm import Session
from .models import SeismologyExperiment, SeismologyFinding, SeismologyDataPoint
from .schemas import SeismologyExperimentCreate, SeismologyExperimentUpdate, SeismologyFindingCreate, SeismologyDataPointCreate
from typing import List, Optional

class SeismologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SeismologyExperiment]:
        return self.db.query(SeismologyExperiment).filter(SeismologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SeismologyExperiment]:
        return self.db.query(SeismologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SeismologyExperimentCreate) -> SeismologyExperiment:
        db_exp = SeismologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SeismologyExperimentUpdate) -> Optional[SeismologyExperiment]:
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

    def create_finding(self, finding_in: SeismologyFindingCreate) -> SeismologyFinding:
        db_finding = SeismologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SeismologyFinding]:
        return self.db.query(SeismologyFinding).filter(SeismologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SeismologyDataPointCreate) -> SeismologyDataPoint:
        db_dp = SeismologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SeismologyDataPoint]:
        return self.db.query(SeismologyDataPoint).filter(SeismologyDataPoint.experiment_id == experiment_id).all()
