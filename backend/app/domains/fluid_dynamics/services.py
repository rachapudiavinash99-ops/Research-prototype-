from sqlalchemy.orm import Session
from .models import FluidDynamicsExperiment, FluidDynamicsFinding, FluidDynamicsDataPoint
from .schemas import FluidDynamicsExperimentCreate, FluidDynamicsExperimentUpdate, FluidDynamicsFindingCreate, FluidDynamicsDataPointCreate
from typing import List, Optional

class FluidDynamicsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[FluidDynamicsExperiment]:
        return self.db.query(FluidDynamicsExperiment).filter(FluidDynamicsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[FluidDynamicsExperiment]:
        return self.db.query(FluidDynamicsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: FluidDynamicsExperimentCreate) -> FluidDynamicsExperiment:
        db_exp = FluidDynamicsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: FluidDynamicsExperimentUpdate) -> Optional[FluidDynamicsExperiment]:
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

    def create_finding(self, finding_in: FluidDynamicsFindingCreate) -> FluidDynamicsFinding:
        db_finding = FluidDynamicsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[FluidDynamicsFinding]:
        return self.db.query(FluidDynamicsFinding).filter(FluidDynamicsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: FluidDynamicsDataPointCreate) -> FluidDynamicsDataPoint:
        db_dp = FluidDynamicsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[FluidDynamicsDataPoint]:
        return self.db.query(FluidDynamicsDataPoint).filter(FluidDynamicsDataPoint.experiment_id == experiment_id).all()
