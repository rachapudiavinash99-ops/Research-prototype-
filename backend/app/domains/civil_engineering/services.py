from sqlalchemy.orm import Session
from .models import CivilEngineeringExperiment, CivilEngineeringFinding, CivilEngineeringDataPoint
from .schemas import CivilEngineeringExperimentCreate, CivilEngineeringExperimentUpdate, CivilEngineeringFindingCreate, CivilEngineeringDataPointCreate
from typing import List, Optional

class CivilEngineeringService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[CivilEngineeringExperiment]:
        return self.db.query(CivilEngineeringExperiment).filter(CivilEngineeringExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[CivilEngineeringExperiment]:
        return self.db.query(CivilEngineeringExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: CivilEngineeringExperimentCreate) -> CivilEngineeringExperiment:
        db_exp = CivilEngineeringExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: CivilEngineeringExperimentUpdate) -> Optional[CivilEngineeringExperiment]:
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

    def create_finding(self, finding_in: CivilEngineeringFindingCreate) -> CivilEngineeringFinding:
        db_finding = CivilEngineeringFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[CivilEngineeringFinding]:
        return self.db.query(CivilEngineeringFinding).filter(CivilEngineeringFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: CivilEngineeringDataPointCreate) -> CivilEngineeringDataPoint:
        db_dp = CivilEngineeringDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[CivilEngineeringDataPoint]:
        return self.db.query(CivilEngineeringDataPoint).filter(CivilEngineeringDataPoint.experiment_id == experiment_id).all()
