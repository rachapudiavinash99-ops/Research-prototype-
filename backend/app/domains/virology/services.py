from sqlalchemy.orm import Session
from .models import VirologyExperiment, VirologyFinding, VirologyDataPoint
from .schemas import VirologyExperimentCreate, VirologyExperimentUpdate, VirologyFindingCreate, VirologyDataPointCreate
from typing import List, Optional

class VirologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[VirologyExperiment]:
        return self.db.query(VirologyExperiment).filter(VirologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[VirologyExperiment]:
        return self.db.query(VirologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: VirologyExperimentCreate) -> VirologyExperiment:
        db_exp = VirologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: VirologyExperimentUpdate) -> Optional[VirologyExperiment]:
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

    def create_finding(self, finding_in: VirologyFindingCreate) -> VirologyFinding:
        db_finding = VirologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[VirologyFinding]:
        return self.db.query(VirologyFinding).filter(VirologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: VirologyDataPointCreate) -> VirologyDataPoint:
        db_dp = VirologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[VirologyDataPoint]:
        return self.db.query(VirologyDataPoint).filter(VirologyDataPoint.experiment_id == experiment_id).all()
