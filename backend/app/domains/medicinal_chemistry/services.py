from sqlalchemy.orm import Session
from .models import MedicinalChemistryExperiment, MedicinalChemistryFinding, MedicinalChemistryDataPoint
from .schemas import MedicinalChemistryExperimentCreate, MedicinalChemistryExperimentUpdate, MedicinalChemistryFindingCreate, MedicinalChemistryDataPointCreate
from typing import List, Optional

class MedicinalChemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MedicinalChemistryExperiment]:
        return self.db.query(MedicinalChemistryExperiment).filter(MedicinalChemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MedicinalChemistryExperiment]:
        return self.db.query(MedicinalChemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MedicinalChemistryExperimentCreate) -> MedicinalChemistryExperiment:
        db_exp = MedicinalChemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MedicinalChemistryExperimentUpdate) -> Optional[MedicinalChemistryExperiment]:
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

    def create_finding(self, finding_in: MedicinalChemistryFindingCreate) -> MedicinalChemistryFinding:
        db_finding = MedicinalChemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MedicinalChemistryFinding]:
        return self.db.query(MedicinalChemistryFinding).filter(MedicinalChemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MedicinalChemistryDataPointCreate) -> MedicinalChemistryDataPoint:
        db_dp = MedicinalChemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MedicinalChemistryDataPoint]:
        return self.db.query(MedicinalChemistryDataPoint).filter(MedicinalChemistryDataPoint.experiment_id == experiment_id).all()
