from sqlalchemy.orm import Session
from .models import InorganicChemistryExperiment, InorganicChemistryFinding, InorganicChemistryDataPoint
from .schemas import InorganicChemistryExperimentCreate, InorganicChemistryExperimentUpdate, InorganicChemistryFindingCreate, InorganicChemistryDataPointCreate
from typing import List, Optional

class InorganicChemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[InorganicChemistryExperiment]:
        return self.db.query(InorganicChemistryExperiment).filter(InorganicChemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[InorganicChemistryExperiment]:
        return self.db.query(InorganicChemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: InorganicChemistryExperimentCreate) -> InorganicChemistryExperiment:
        db_exp = InorganicChemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: InorganicChemistryExperimentUpdate) -> Optional[InorganicChemistryExperiment]:
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

    def create_finding(self, finding_in: InorganicChemistryFindingCreate) -> InorganicChemistryFinding:
        db_finding = InorganicChemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[InorganicChemistryFinding]:
        return self.db.query(InorganicChemistryFinding).filter(InorganicChemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: InorganicChemistryDataPointCreate) -> InorganicChemistryDataPoint:
        db_dp = InorganicChemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[InorganicChemistryDataPoint]:
        return self.db.query(InorganicChemistryDataPoint).filter(InorganicChemistryDataPoint.experiment_id == experiment_id).all()
