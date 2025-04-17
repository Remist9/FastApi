from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
from configs.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    login = Column(String(50), unique=True, nullable=False)
    password = Column(String, nullable=False)
    firstname = Column(String(100))
    surname = Column(String(100))
    location = Column(String(100))
    registration_time = Column(DateTime, default=datetime.utcnow)
    last_auth_time = Column(DateTime, default=datetime.utcnow)
