from sqlalchemy.orm import Session
from .models import EducationExperiment, EducationFinding, EducationDataPoint
from .schemas import EducationExperimentCreate, EducationExperimentUpdate, EducationFindingCreate, EducationDataPointCreate
from typing import List, Optional

class EducationService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[EducationExperiment]:
        return self.db.query(EducationExperiment).filter(EducationExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[EducationExperiment]:
        return self.db.query(EducationExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: EducationExperimentCreate) -> EducationExperiment:
        db_exp = EducationExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: EducationExperimentUpdate) -> Optional[EducationExperiment]:
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

    def create_finding(self, finding_in: EducationFindingCreate) -> EducationFinding:
        db_finding = EducationFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[EducationFinding]:
        return self.db.query(EducationFinding).filter(EducationFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: EducationDataPointCreate) -> EducationDataPoint:
        db_dp = EducationDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[EducationDataPoint]:
        return self.db.query(EducationDataPoint).filter(EducationDataPoint.experiment_id == experiment_id).all()
