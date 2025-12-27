from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from datetime import datetime

Base = declarative_base()

class Alert(Base):
    __tablename__ = "alerts"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    source = Column(String, index=True)
    severity = Column(String) # Low, Medium, High
    status = Column(String, default="Open")
    mitre_ttp = Column(String, nullable=True)
    explanation = Column(Text)

class Action(Base):
    __tablename__ = "actions"

    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(Integer, ForeignKey("alerts.id"))
    action_taken = Column(String)
    success = Column(Boolean, default=False)
    executor = Column(String)
    timestamp = Column(DateTime, default=datetime.utcnow)

    alert = relationship("Alert")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(String, default="Analyst")
    phone = Column(String, nullable=True)
