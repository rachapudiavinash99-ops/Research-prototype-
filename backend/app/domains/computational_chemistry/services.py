from sqlalchemy.orm import Session
from .models import ComputationalChemistryExperiment, ComputationalChemistryFinding, ComputationalChemistryDataPoint
from .schemas import ComputationalChemistryExperimentCreate, ComputationalChemistryExperimentUpdate, ComputationalChemistryFindingCreate, ComputationalChemistryDataPointCreate
from typing import List, Optional

class ComputationalChemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ComputationalChemistryExperiment]:
        return self.db.query(ComputationalChemistryExperiment).filter(ComputationalChemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ComputationalChemistryExperiment]:
        return self.db.query(ComputationalChemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ComputationalChemistryExperimentCreate) -> ComputationalChemistryExperiment:
        db_exp = ComputationalChemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ComputationalChemistryExperimentUpdate) -> Optional[ComputationalChemistryExperiment]:
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

    def create_finding(self, finding_in: ComputationalChemistryFindingCreate) -> ComputationalChemistryFinding:
        db_finding = ComputationalChemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ComputationalChemistryFinding]:
        return self.db.query(ComputationalChemistryFinding).filter(ComputationalChemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ComputationalChemistryDataPointCreate) -> ComputationalChemistryDataPoint:
        db_dp = ComputationalChemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ComputationalChemistryDataPoint]:
        return self.db.query(ComputationalChemistryDataPoint).filter(ComputationalChemistryDataPoint.experiment_id == experiment_id).all()
