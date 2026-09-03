from sqlalchemy.orm import Session
from .models import BioinformaticsExperiment, BioinformaticsFinding, BioinformaticsDataPoint
from .schemas import BioinformaticsExperimentCreate, BioinformaticsExperimentUpdate, BioinformaticsFindingCreate, BioinformaticsDataPointCreate
from typing import List, Optional

class BioinformaticsService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[BioinformaticsExperiment]:
        return self.db.query(BioinformaticsExperiment).filter(BioinformaticsExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[BioinformaticsExperiment]:
        return self.db.query(BioinformaticsExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: BioinformaticsExperimentCreate) -> BioinformaticsExperiment:
        db_exp = BioinformaticsExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: BioinformaticsExperimentUpdate) -> Optional[BioinformaticsExperiment]:
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

    def create_finding(self, finding_in: BioinformaticsFindingCreate) -> BioinformaticsFinding:
        db_finding = BioinformaticsFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[BioinformaticsFinding]:
        return self.db.query(BioinformaticsFinding).filter(BioinformaticsFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: BioinformaticsDataPointCreate) -> BioinformaticsDataPoint:
        db_dp = BioinformaticsDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[BioinformaticsDataPoint]:
        return self.db.query(BioinformaticsDataPoint).filter(BioinformaticsDataPoint.experiment_id == experiment_id).all()
