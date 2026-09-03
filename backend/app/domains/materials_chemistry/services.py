from sqlalchemy.orm import Session
from .models import MaterialsChemistryExperiment, MaterialsChemistryFinding, MaterialsChemistryDataPoint
from .schemas import MaterialsChemistryExperimentCreate, MaterialsChemistryExperimentUpdate, MaterialsChemistryFindingCreate, MaterialsChemistryDataPointCreate
from typing import List, Optional

class MaterialsChemistryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[MaterialsChemistryExperiment]:
        return self.db.query(MaterialsChemistryExperiment).filter(MaterialsChemistryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[MaterialsChemistryExperiment]:
        return self.db.query(MaterialsChemistryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: MaterialsChemistryExperimentCreate) -> MaterialsChemistryExperiment:
        db_exp = MaterialsChemistryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: MaterialsChemistryExperimentUpdate) -> Optional[MaterialsChemistryExperiment]:
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

    def create_finding(self, finding_in: MaterialsChemistryFindingCreate) -> MaterialsChemistryFinding:
        db_finding = MaterialsChemistryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[MaterialsChemistryFinding]:
        return self.db.query(MaterialsChemistryFinding).filter(MaterialsChemistryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: MaterialsChemistryDataPointCreate) -> MaterialsChemistryDataPoint:
        db_dp = MaterialsChemistryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[MaterialsChemistryDataPoint]:
        return self.db.query(MaterialsChemistryDataPoint).filter(MaterialsChemistryDataPoint.experiment_id == experiment_id).all()
