from fastapi import Depends
from sqlalchemy.orm import Session
from app.db.session import SessionLocal
from app.models.user import User

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(db: Session = Depends(get_db)):
    fake_user = db.query(User).first()
    if not fake_user:
        fake_user = User(id=1, email="test@test.com", hashed_password="fake", is_active=True)
        db.add(fake_user)
        db.commit()
    return fake_user

def get_current_active_user(current_user: User = Depends(get_current_user)):
    return current_user
