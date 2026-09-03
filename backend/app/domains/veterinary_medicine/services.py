from sqlalchemy.orm import Session
from .models import VeterinaryMedicineExperiment, VeterinaryMedicineFinding, VeterinaryMedicineDataPoint
from .schemas import VeterinaryMedicineExperimentCreate, VeterinaryMedicineExperimentUpdate, VeterinaryMedicineFindingCreate, VeterinaryMedicineDataPointCreate
from typing import List, Optional

class VeterinaryMedicineService:
    def __init__(self, db: Session):
        self.db = db

    def get_experiment(self, experiment_id: int) -> Optional[VeterinaryMedicineExperiment]:
        return self.db.query(VeterinaryMedicineExperiment).filter(VeterinaryMedicineExperiment.id == experiment_id).first()

    def get_experiments(self, skip: int = 0, limit: int = 100) -> List[VeterinaryMedicineExperiment]:
        return self.db.query(VeterinaryMedicineExperiment).offset(skip).limit(limit).all()

    def create_experiment(self, exp_in: VeterinaryMedicineExperimentCreate) -> VeterinaryMedicineExperiment:
        db_exp = VeterinaryMedicineExperiment(**exp_in.model_dump())
        self.db.add(db_exp)
        self.db.commit()
        self.db.refresh(db_exp)
        return db_exp

    def update_experiment(self, experiment_id: int, exp_in: VeterinaryMedicineExperimentUpdate) -> Optional[VeterinaryMedicineExperiment]:
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

    def create_finding(self, finding_in: VeterinaryMedicineFindingCreate) -> VeterinaryMedicineFinding:
        db_finding = VeterinaryMedicineFinding(**finding_in.model_dump())
        self.db.add(db_finding)
        self.db.commit()
        self.db.refresh(db_finding)
        return db_finding
        
    def get_findings(self, experiment_id: int) -> List[VeterinaryMedicineFinding]:
        return self.db.query(VeterinaryMedicineFinding).filter(VeterinaryMedicineFinding.experiment_id == experiment_id).all()
        
    def create_datapoint(self, dp_in: VeterinaryMedicineDataPointCreate) -> VeterinaryMedicineDataPoint:
        db_dp = VeterinaryMedicineDataPoint(**dp_in.model_dump())
        self.db.add(db_dp)
        self.db.commit()
        self.db.refresh(db_dp)
        return db_dp
        
    def get_datapoints(self, experiment_id: int) -> List[VeterinaryMedicineDataPoint]:
        return self.db.query(VeterinaryMedicineDataPoint).filter(VeterinaryMedicineDataPoint.experiment_id == experiment_id).all()
