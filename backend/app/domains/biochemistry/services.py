from sqlalchemy.orm import Session
from .models import BiochemistryExperiment, BiochemistryFinding, BiochemistryDataPoint
from .schemas import BiochemistryExperimentCreate, BiochemistryExperimentUpdate, BiochemistryFindingCreate, BiochemistryDataPointCreate
from typing import List, Optional

class BiochemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[BiochemistryExperiment]:
        return self.db.query(BiochemistryExperiment).filter(BiochemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[BiochemistryExperiment]:
        return self.db.query(BiochemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: BiochemistryExperimentCreate) -> BiochemistryExperiment:
        db_exp = BiochemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: BiochemistryExperimentUpdate) -> Optional[BiochemistryExperiment]:
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

    def create_finding(self, finding_in: BiochemistryFindingCreate) -> BiochemistryFinding:
        db_finding = BiochemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[BiochemistryFinding]:
        return self.db.query(BiochemistryFinding).filter(BiochemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: BiochemistryDataPointCreate) -> BiochemistryDataPoint:
        db_dp = BiochemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[BiochemistryDataPoint]:
        return self.db.query(BiochemistryDataPoint).filter(BiochemistryDataPoint.experiment_id == experiment_id).all()
