from sqlalchemy.orm import Session
from .models import IotExperiment, IotFinding, IotDataPoint
from .schemas import IotExperimentCreate, IotExperimentUpdate, IotFindingCreate, IotDataPointCreate
from typing import List, Optional

class IotService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[IotExperiment]:
        return self.db.query(IotExperiment).filter(IotExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[IotExperiment]:
        return self.db.query(IotExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: IotExperimentCreate) -> IotExperiment:
        db_exp = IotExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: IotExperimentUpdate) -> Optional[IotExperiment]:
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

    def create_finding(self, finding_in: IotFindingCreate) -> IotFinding:
        db_finding = IotFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[IotFinding]:
        return self.db.query(IotFinding).filter(IotFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: IotDataPointCreate) -> IotDataPoint:
        db_dp = IotDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[IotDataPoint]:
        return self.db.query(IotDataPoint).filter(IotDataPoint.experiment_id == experiment_id).all()
