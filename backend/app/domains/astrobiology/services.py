from sqlalchemy.orm import Session
from .models import AstrobiologyExperiment, AstrobiologyFinding, AstrobiologyDataPoint
from .schemas import AstrobiologyExperimentCreate, AstrobiologyExperimentUpdate, AstrobiologyFindingCreate, AstrobiologyDataPointCreate
from typing import List, Optional

class AstrobiologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AstrobiologyExperiment]:
        return self.db.query(AstrobiologyExperiment).filter(AstrobiologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AstrobiologyExperiment]:
        return self.db.query(AstrobiologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AstrobiologyExperimentCreate) -> AstrobiologyExperiment:
        db_exp = AstrobiologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AstrobiologyExperimentUpdate) -> Optional[AstrobiologyExperiment]:
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

    def create_finding(self, finding_in: AstrobiologyFindingCreate) -> AstrobiologyFinding:
        db_finding = AstrobiologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AstrobiologyFinding]:
        return self.db.query(AstrobiologyFinding).filter(AstrobiologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AstrobiologyDataPointCreate) -> AstrobiologyDataPoint:
        db_dp = AstrobiologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AstrobiologyDataPoint]:
        return self.db.query(AstrobiologyDataPoint).filter(AstrobiologyDataPoint.experiment_id == experiment_id).all()
