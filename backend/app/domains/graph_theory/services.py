from sqlalchemy.orm import Session
from .models import GraphTheoryExperiment, GraphTheoryFinding, GraphTheoryDataPoint
from .schemas import GraphTheoryExperimentCreate, GraphTheoryExperimentUpdate, GraphTheoryFindingCreate, GraphTheoryDataPointCreate
from typing import List, Optional

class GraphTheoryService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[GraphTheoryExperiment]:
        return self.db.query(GraphTheoryExperiment).filter(GraphTheoryExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[GraphTheoryExperiment]:
        return self.db.query(GraphTheoryExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: GraphTheoryExperimentCreate) -> GraphTheoryExperiment:
        db_exp = GraphTheoryExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: GraphTheoryExperimentUpdate) -> Optional[GraphTheoryExperiment]:
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

    def create_finding(self, finding_in: GraphTheoryFindingCreate) -> GraphTheoryFinding:
        db_finding = GraphTheoryFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[GraphTheoryFinding]:
        return self.db.query(GraphTheoryFinding).filter(GraphTheoryFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: GraphTheoryDataPointCreate) -> GraphTheoryDataPoint:
        db_dp = GraphTheoryDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[GraphTheoryDataPoint]:
        return self.db.query(GraphTheoryDataPoint).filter(GraphTheoryDataPoint.experiment_id == experiment_id).all()
