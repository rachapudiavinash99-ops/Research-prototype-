from sqlalchemy.orm import Session
from .models import SystemsPharmacologyExperiment, SystemsPharmacologyFinding, SystemsPharmacologyDataPoint
from .schemas import SystemsPharmacologyExperimentCreate, SystemsPharmacologyExperimentUpdate, SystemsPharmacologyFindingCreate, SystemsPharmacologyDataPointCreate
from typing import List, Optional

class SystemsPharmacologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[SystemsPharmacologyExperiment]:
        return self.db.query(SystemsPharmacologyExperiment).filter(SystemsPharmacologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[SystemsPharmacologyExperiment]:
        return self.db.query(SystemsPharmacologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: SystemsPharmacologyExperimentCreate) -> SystemsPharmacologyExperiment:
        db_exp = SystemsPharmacologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: SystemsPharmacologyExperimentUpdate) -> Optional[SystemsPharmacologyExperiment]:
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

    def create_finding(self, finding_in: SystemsPharmacologyFindingCreate) -> SystemsPharmacologyFinding:
        db_finding = SystemsPharmacologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[SystemsPharmacologyFinding]:
        return self.db.query(SystemsPharmacologyFinding).filter(SystemsPharmacologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: SystemsPharmacologyDataPointCreate) -> SystemsPharmacologyDataPoint:
        db_dp = SystemsPharmacologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[SystemsPharmacologyDataPoint]:
        return self.db.query(SystemsPharmacologyDataPoint).filter(SystemsPharmacologyDataPoint.experiment_id == experiment_id).all()
