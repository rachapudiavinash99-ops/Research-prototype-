from sqlalchemy.orm import Session
from .models import ChemistryExperiment, ChemistryFinding, ChemistryDataPoint
from .schemas import ChemistryExperimentCreate, ChemistryExperimentUpdate, ChemistryFindingCreate, ChemistryDataPointCreate
from typing import List, Optional

class ChemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ChemistryExperiment]:
        return self.db.query(ChemistryExperiment).filter(ChemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ChemistryExperiment]:
        return self.db.query(ChemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ChemistryExperimentCreate) -> ChemistryExperiment:
        db_exp = ChemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ChemistryExperimentUpdate) -> Optional[ChemistryExperiment]:
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

    def create_finding(self, finding_in: ChemistryFindingCreate) -> ChemistryFinding:
        db_finding = ChemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ChemistryFinding]:
        return self.db.query(ChemistryFinding).filter(ChemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ChemistryDataPointCreate) -> ChemistryDataPoint:
        db_dp = ChemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ChemistryDataPoint]:
        return self.db.query(ChemistryDataPoint).filter(ChemistryDataPoint.experiment_id == experiment_id).all()
