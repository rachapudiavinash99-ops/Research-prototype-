from sqlalchemy.orm import Session
from .models import TopologyExperiment, TopologyFinding, TopologyDataPoint
from .schemas import TopologyExperimentCreate, TopologyExperimentUpdate, TopologyFindingCreate, TopologyDataPointCreate
from typing import List, Optional

class TopologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[TopologyExperiment]:
        return self.db.query(TopologyExperiment).filter(TopologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[TopologyExperiment]:
        return self.db.query(TopologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: TopologyExperimentCreate) -> TopologyExperiment:
        db_exp = TopologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: TopologyExperimentUpdate) -> Optional[TopologyExperiment]:
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

    def create_finding(self, finding_in: TopologyFindingCreate) -> TopologyFinding:
        db_finding = TopologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[TopologyFinding]:
        return self.db.query(TopologyFinding).filter(TopologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: TopologyDataPointCreate) -> TopologyDataPoint:
        db_dp = TopologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[TopologyDataPoint]:
        return self.db.query(TopologyDataPoint).filter(TopologyDataPoint.experiment_id == experiment_id).all()
