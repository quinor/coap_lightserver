from sqlalchemy import create_engine, Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base

import settings
import minclient
import datetime


engine = create_engine(settings.db_file)
Session = sessionmaker(bind=engine)
Base = declarative_base()

def duckduckgogo(path, op, payload=None):
    print("{}, {}, {}".format(path, op, payload))

class Light(Base):
    __tablename__ = "lights"

    dev_id      = Column(String(100), unique=True, primary_key=True)
    timestamp   = Column(DateTime)
    # devices

    def refresh(self):
        minclient.send(
            "coap://{}:{}/pilot/{}".format(
                settings.fwd_proxy_ip,
                settings.fwd_proxy_port,
                self.dev_id
            ),
            "PUT",
            "OFF" if self.active_for() == -1 else "ON",
            timeout=0.05,
        )

    def active_for(self):
        ret = int((self.timestamp - datetime.datetime.now()).total_seconds())
        if ret <= 0:
            return -1
        return ret

    def activate_for(self, t):
        self.timestamp = max(
            self.timestamp, datetime.datetime.now() + datetime.timedelta(seconds=t))


    def deactivate(self):
        self.timestamp = datetime.datetime.now()

class Device(Base):
    __tablename__ = "devices"

    dev_id      = Column(String(100), unique=True, primary_key=True)
    length      = Column(Integer)
    timestamp   = Column(DateTime)
    enabled     = Column(Boolean)
    light_id    = Column(String(100), ForeignKey(Light.dev_id))
    light       = relationship(Light, backref="devices")
