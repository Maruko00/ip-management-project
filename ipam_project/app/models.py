from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base

class Subnet(Base):
    __tablename__ = "subnets"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    network_address = Column(String, nullable=False, unique=True, index=True)
    description = Column(Text, nullable=True)
    parent_subnet_id = Column(Integer, ForeignKey("subnets.id"), nullable=True)

    parent_subnet = relationship("Subnet", remote_side=[id], back_populates="child_subnets")
    child_subnets = relationship("Subnet", back_populates="parent_subnet")
    ip_addresses = relationship("IPAddress", back_populates="subnet")

class IPAddress(Base):
    __tablename__ = "ip_addresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    ip_address = Column(String, nullable=False, unique=True, index=True)
    subnet_id = Column(Integer, ForeignKey("subnets.id"), nullable=False)
    status = Column(String, nullable=False, default="Free") # e.g., "Used", "Free", "Reserved"
    hostname = Column(String, nullable=True)
    mac_address = Column(String, nullable=True, unique=True)
    notes = Column(Text, nullable=True)

    subnet = relationship("Subnet", back_populates="ip_addresses")
