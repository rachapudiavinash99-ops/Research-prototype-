from sqlalchemy.orm import Session
from .models import AnthropologyExperiment, AnthropologyFinding, AnthropologyDataPoint
from .schemas import AnthropologyExperimentCreate, AnthropologyExperimentUpdate, AnthropologyFindingCreate, AnthropologyDataPointCreate
from typing import List, Optional

class AnthropologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[AnthropologyExperiment]:
        return self.db.query(AnthropologyExperiment).filter(AnthropologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[AnthropologyExperiment]:
        return self.db.query(AnthropologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: AnthropologyExperimentCreate) -> AnthropologyExperiment:
        db_exp = AnthropologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: AnthropologyExperimentUpdate) -> Optional[AnthropologyExperiment]:
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

    def create_finding(self, finding_in: AnthropologyFindingCreate) -> AnthropologyFinding:
        db_finding = AnthropologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[AnthropologyFinding]:
        return self.db.query(AnthropologyFinding).filter(AnthropologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: AnthropologyDataPointCreate) -> AnthropologyDataPoint:
        db_dp = AnthropologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[AnthropologyDataPoint]:
        return self.db.query(AnthropologyDataPoint).filter(AnthropologyDataPoint.experiment_id == experiment_id).all()
