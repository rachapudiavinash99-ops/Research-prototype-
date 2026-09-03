from sqlalchemy.orm import Session
from .models import GreenChemistryExperiment, GreenChemistryFinding, GreenChemistryDataPoint
from .schemas import GreenChemistryExperimentCreate, GreenChemistryExperimentUpdate, GreenChemistryFindingCreate, GreenChemistryDataPointCreate
from typing import List, Optional

class GreenChemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[GreenChemistryExperiment]:
        return self.db.query(GreenChemistryExperiment).filter(GreenChemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[GreenChemistryExperiment]:
        return self.db.query(GreenChemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: GreenChemistryExperimentCreate) -> GreenChemistryExperiment:
        db_exp = GreenChemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: GreenChemistryExperimentUpdate) -> Optional[GreenChemistryExperiment]:
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

    def create_finding(self, finding_in: GreenChemistryFindingCreate) -> GreenChemistryFinding:
        db_finding = GreenChemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[GreenChemistryFinding]:
        return self.db.query(GreenChemistryFinding).filter(GreenChemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: GreenChemistryDataPointCreate) -> GreenChemistryDataPoint:
        db_dp = GreenChemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[GreenChemistryDataPoint]:
        return self.db.query(GreenChemistryDataPoint).filter(GreenChemistryDataPoint.experiment_id == experiment_id).all()
