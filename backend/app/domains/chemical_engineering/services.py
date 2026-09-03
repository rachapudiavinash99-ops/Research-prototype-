from sqlalchemy.orm import Session
from .models import ChemicalEngineeringExperiment, ChemicalEngineeringFinding, ChemicalEngineeringDataPoint
from .schemas import ChemicalEngineeringExperimentCreate, ChemicalEngineeringExperimentUpdate, ChemicalEngineeringFindingCreate, ChemicalEngineeringDataPointCreate
from typing import List, Optional

class ChemicalEngineeringService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[ChemicalEngineeringExperiment]:
        return self.db.query(ChemicalEngineeringExperiment).filter(ChemicalEngineeringExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[ChemicalEngineeringExperiment]:
        return self.db.query(ChemicalEngineeringExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: ChemicalEngineeringExperimentCreate) -> ChemicalEngineeringExperiment:
        db_exp = ChemicalEngineeringExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: ChemicalEngineeringExperimentUpdate) -> Optional[ChemicalEngineeringExperiment]:
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

    def create_finding(self, finding_in: ChemicalEngineeringFindingCreate) -> ChemicalEngineeringFinding:
        db_finding = ChemicalEngineeringFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[ChemicalEngineeringFinding]:
        return self.db.query(ChemicalEngineeringFinding).filter(ChemicalEngineeringFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: ChemicalEngineeringDataPointCreate) -> ChemicalEngineeringDataPoint:
        db_dp = ChemicalEngineeringDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[ChemicalEngineeringDataPoint]:
        return self.db.query(ChemicalEngineeringDataPoint).filter(ChemicalEngineeringDataPoint.experiment_id == experiment_id).all()
