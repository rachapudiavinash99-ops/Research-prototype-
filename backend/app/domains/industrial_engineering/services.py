from sqlalchemy.orm import Session
from .models import IndustrialEngineeringExperiment, IndustrialEngineeringFinding, IndustrialEngineeringDataPoint
from .schemas import IndustrialEngineeringExperimentCreate, IndustrialEngineeringExperimentUpdate, IndustrialEngineeringFindingCreate, IndustrialEngineeringDataPointCreate
from typing import List, Optional

class IndustrialEngineeringService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[IndustrialEngineeringExperiment]:
        return self.db.query(IndustrialEngineeringExperiment).filter(IndustrialEngineeringExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[IndustrialEngineeringExperiment]:
        return self.db.query(IndustrialEngineeringExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: IndustrialEngineeringExperimentCreate) -> IndustrialEngineeringExperiment:
        db_exp = IndustrialEngineeringExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: IndustrialEngineeringExperimentUpdate) -> Optional[IndustrialEngineeringExperiment]:
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

    def create_finding(self, finding_in: IndustrialEngineeringFindingCreate) -> IndustrialEngineeringFinding:
        db_finding = IndustrialEngineeringFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[IndustrialEngineeringFinding]:
        return self.db.query(IndustrialEngineeringFinding).filter(IndustrialEngineeringFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: IndustrialEngineeringDataPointCreate) -> IndustrialEngineeringDataPoint:
        db_dp = IndustrialEngineeringDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[IndustrialEngineeringDataPoint]:
        return self.db.query(IndustrialEngineeringDataPoint).filter(IndustrialEngineeringDataPoint.experiment_id == experiment_id).all()
