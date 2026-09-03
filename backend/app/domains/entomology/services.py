from sqlalchemy.orm import Session
from .models import EntomologyExperiment, EntomologyFinding, EntomologyDataPoint
from .schemas import EntomologyExperimentCreate, EntomologyExperimentUpdate, EntomologyFindingCreate, EntomologyDataPointCreate
from typing import List, Optional

class EntomologyService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[EntomologyExperiment]:
        return self.db.query(EntomologyExperiment).filter(EntomologyExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[EntomologyExperiment]:
        return self.db.query(EntomologyExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: EntomologyExperimentCreate) -> EntomologyExperiment:
        db_exp = EntomologyExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: EntomologyExperimentUpdate) -> Optional[EntomologyExperiment]:
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

    def create_finding(self, finding_in: EntomologyFindingCreate) -> EntomologyFinding:
        db_finding = EntomologyFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[EntomologyFinding]:
        return self.db.query(EntomologyFinding).filter(EntomologyFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: EntomologyDataPointCreate) -> EntomologyDataPoint:
        db_dp = EntomologyDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[EntomologyDataPoint]:
        return self.db.query(EntomologyDataPoint).filter(EntomologyDataPoint.experiment_id == experiment_id).all()
