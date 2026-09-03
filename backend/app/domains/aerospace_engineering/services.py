from sqlalchemy.orm import Session
from .models import AerospaceEngineeringExperiment, AerospaceEngineeringFinding, AerospaceEngineeringDataPoint
from .schemas import AerospaceEngineeringExperimentCreate, AerospaceEngineeringExperimentUpdate, AerospaceEngineeringFindingCreate, AerospaceEngineeringDataPointCreate
from typing import List, Optional

class AerospaceEngineeringService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AerospaceEngineeringExperiment]:
        return self.db.query(AerospaceEngineeringExperiment).filter(AerospaceEngineeringExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AerospaceEngineeringExperiment]:
        return self.db.query(AerospaceEngineeringExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AerospaceEngineeringExperimentCreate) -> AerospaceEngineeringExperiment:
        db_exp = AerospaceEngineeringExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AerospaceEngineeringExperimentUpdate) -> Optional[AerospaceEngineeringExperiment]:
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

    def create_finding(self, finding_in: AerospaceEngineeringFindingCreate) -> AerospaceEngineeringFinding:
        db_finding = AerospaceEngineeringFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AerospaceEngineeringFinding]:
        return self.db.query(AerospaceEngineeringFinding).filter(AerospaceEngineeringFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AerospaceEngineeringDataPointCreate) -> AerospaceEngineeringDataPoint:
        db_dp = AerospaceEngineeringDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AerospaceEngineeringDataPoint]:
        return self.db.query(AerospaceEngineeringDataPoint).filter(AerospaceEngineeringDataPoint.experiment_id == experiment_id).all()
