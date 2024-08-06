from sqlalchemy import Column, String, Integer, Boolean
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TransportUnit(Base):
    __tablename__ = 'transport_units'
    id = Column(String, primary_key=True)
    color = Column(String)
    type = Column(String)
    weight = Column(Integer)
    height = Column(Integer)
    length = Column(Integer)
    width = Column(Integer)
    current_loc = Column(String)
    outbound_request = Column(Boolean)


class Warehouse(Base):
    __tablename__ = 'warehouse'
    y = Column(Integer, primary_key=True)
    x = Column(Integer, primary_key=True)
    direction = Column(String, primary_key=True)
    seat_id = Column(String)
    status = Column(String)
