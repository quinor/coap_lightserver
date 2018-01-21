from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from settings import db_file


engine = create_engine(db_file)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Device(Base):
    __tablename__ = "devices"

    id          = Column(Integer, primary_key=True)
    dev_id      = Column(String(100), unique=True)
    length      = Column(Integer)
    timestamp   = Column(DateTime)
    enabled     = Column(Boolean)
