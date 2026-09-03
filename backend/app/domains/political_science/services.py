from sqlalchemy.orm import Session
from .models import PoliticalScienceExperiment, PoliticalScienceFinding, PoliticalScienceDataPoint
from .schemas import PoliticalScienceExperimentCreate, PoliticalScienceExperimentUpdate, PoliticalScienceFindingCreate, PoliticalScienceDataPointCreate
from typing import List, Optional

class PoliticalScienceService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[PoliticalScienceExperiment]:
        return self.db.query(PoliticalScienceExperiment).filter(PoliticalScienceExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[PoliticalScienceExperiment]:
        return self.db.query(PoliticalScienceExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: PoliticalScienceExperimentCreate) -> PoliticalScienceExperiment:
        db_exp = PoliticalScienceExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: PoliticalScienceExperimentUpdate) -> Optional[PoliticalScienceExperiment]:
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

    def create_finding(self, finding_in: PoliticalScienceFindingCreate) -> PoliticalScienceFinding:
        db_finding = PoliticalScienceFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[PoliticalScienceFinding]:
        return self.db.query(PoliticalScienceFinding).filter(PoliticalScienceFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: PoliticalScienceDataPointCreate) -> PoliticalScienceDataPoint:
        db_dp = PoliticalScienceDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[PoliticalScienceDataPoint]:
        return self.db.query(PoliticalScienceDataPoint).filter(PoliticalScienceDataPoint.experiment_id == experiment_id).all()
