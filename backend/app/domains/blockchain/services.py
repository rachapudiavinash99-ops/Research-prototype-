from sqlalchemy.orm import Session
from .models import BlockchainExperiment, BlockchainFinding, BlockchainDataPoint
from .schemas import BlockchainExperimentCreate, BlockchainExperimentUpdate, BlockchainFindingCreate, BlockchainDataPointCreate
from typing import List, Optional

class BlockchainService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[BlockchainExperiment]:
        return self.db.query(BlockchainExperiment).filter(BlockchainExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[BlockchainExperiment]:
        return self.db.query(BlockchainExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: BlockchainExperimentCreate) -> BlockchainExperiment:
        db_exp = BlockchainExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: BlockchainExperimentUpdate) -> Optional[BlockchainExperiment]:
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

    def create_finding(self, finding_in: BlockchainFindingCreate) -> BlockchainFinding:
        db_finding = BlockchainFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[BlockchainFinding]:
        return self.db.query(BlockchainFinding).filter(BlockchainFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: BlockchainDataPointCreate) -> BlockchainDataPoint:
        db_dp = BlockchainDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[BlockchainDataPoint]:
        return self.db.query(BlockchainDataPoint).filter(BlockchainDataPoint.experiment_id == experiment_id).all()
