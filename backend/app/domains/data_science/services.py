from sqlalchemy.orm import Session
from .models import DataScienceExperiment, DataScienceFinding, DataScienceDataPoint
from .schemas import DataScienceExperimentCreate, DataScienceExperimentUpdate, DataScienceFindingCreate, DataScienceDataPointCreate
from typing import List, Optional

class DataScienceService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[DataScienceExperiment]:
        return self.db.query(DataScienceExperiment).filter(DataScienceExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[DataScienceExperiment]:
        return self.db.query(DataScienceExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: DataScienceExperimentCreate) -> DataScienceExperiment:
        db_exp = DataScienceExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: DataScienceExperimentUpdate) -> Optional[DataScienceExperiment]:
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

    def create_finding(self, finding_in: DataScienceFindingCreate) -> DataScienceFinding:
        db_finding = DataScienceFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[DataScienceFinding]:
        return self.db.query(DataScienceFinding).filter(DataScienceFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: DataScienceDataPointCreate) -> DataScienceDataPoint:
        db_dp = DataScienceDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[DataScienceDataPoint]:
        return self.db.query(DataScienceDataPoint).filter(DataScienceDataPoint.experiment_id == experiment_id).all()
