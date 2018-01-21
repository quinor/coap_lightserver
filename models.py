from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from settings import db_file

import datetime


engine = create_engine(db_file)
Session = sessionmaker(bind=engine)
Base = declarative_base()


# joint for triggers and toggles
class Device(Base):
    __tablename__ = "devices"

    id          = Column(Integer, primary_key=True)
    dev_id      = Column(String(100), unique=True)
    length      = Column(Integer)
    timestamp   = Column(DateTime)
    enabled     = Column(Boolean)

# only one light!
class Light(Base):
    __tablename__ = "lights"

    id          = Column(Integer, primary_key=True)
    timestamp   = Column(DateTime)

    def active_for(self):
        ret = int((self.timestamp - datetime.datetime.now()).total_seconds())
        if ret <= 0:
            return -1
        return ret

    def activate_for(self, t):
        self.timestamp = datetime.datetime.now() + datetime.timedelta(seconds=t)

    def deactivate(self):
        self.activate_for(0)
