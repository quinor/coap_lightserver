from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

from settings import db_file

import datetime


engine = create_engine(db_file)
Session = sessionmaker(bind=engine)
Base = declarative_base()


class Light(Base):
    __tablename__ = "lights"

    dev_id      = Column(String(100), unique=True, primary_key=True)
    timestamp   = Column(DateTime)
    # devices

    def active_for(self):
        ret = int((self.timestamp - datetime.datetime.now()).total_seconds())
        if ret <= 0:
            return -1
        return ret

    def activate_for(self, t):
        self.timestamp = datetime.datetime.now() + datetime.timedelta(seconds=t)

    def deactivate(self):
        self.activate_for(0)

class Device(Base):
    __tablename__ = "devices"

    dev_id      = Column(String(100), unique=True, primary_key=True)
    length      = Column(Integer)
    timestamp   = Column(DateTime)
    enabled     = Column(Boolean)
    light_id    = Column(String(100), ForeignKey(Light.dev_id))
    light       = relationship(Light, backref="devices")
