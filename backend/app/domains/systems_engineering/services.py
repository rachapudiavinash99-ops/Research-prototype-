from sqlalchemy.orm import Session
from .models import SystemsEngineeringExperiment, SystemsEngineeringFinding, SystemsEngineeringDataPoint
from .schemas import SystemsEngineeringExperimentCreate, SystemsEngineeringExperimentUpdate, SystemsEngineeringFindingCreate, SystemsEngineeringDataPointCreate
from typing import List, Optional

class SystemsEngineeringService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SystemsEngineeringExperiment]:
        return self.db.query(SystemsEngineeringExperiment).filter(SystemsEngineeringExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SystemsEngineeringExperiment]:
        return self.db.query(SystemsEngineeringExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SystemsEngineeringExperimentCreate) -> SystemsEngineeringExperiment:
        db_exp = SystemsEngineeringExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SystemsEngineeringExperimentUpdate) -> Optional[SystemsEngineeringExperiment]:
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

    def create_finding(self, finding_in: SystemsEngineeringFindingCreate) -> SystemsEngineeringFinding:
        db_finding = SystemsEngineeringFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SystemsEngineeringFinding]:
        return self.db.query(SystemsEngineeringFinding).filter(SystemsEngineeringFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SystemsEngineeringDataPointCreate) -> SystemsEngineeringDataPoint:
        db_dp = SystemsEngineeringDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SystemsEngineeringDataPoint]:
        return self.db.query(SystemsEngineeringDataPoint).filter(SystemsEngineeringDataPoint.experiment_id == experiment_id).all()
