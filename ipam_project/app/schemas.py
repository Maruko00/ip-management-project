from pydantic import BaseModel
from typing import Optional, List

# Subnet Schemas
class SubnetBase(BaseModel):
    network_address: str
    description: Optional[str] = None
    parent_subnet_id: Optional[int] = None

class SubnetCreate(SubnetBase):
    pass

class SubnetUpdate(BaseModel):
    network_address: Optional[str] = None
    description: Optional[str] = None
    parent_subnet_id: Optional[int] = None

class Subnet(SubnetBase):
    id: int

    class Config:
        orm_mode = True

# IPAddress Schemas (to be defined later, adding placeholders for now if needed by Subnet schema)
# class IPAddressBase(BaseModel):
#     ip_address: str
#     status: Optional[str] = "Free"
#     hostname: Optional[str] = None
#     mac_address: Optional[str] = None
#     notes: Optional[str] = None

# class IPAddressCreate(IPAddressBase):
#     subnet_id: int

# class IPAddress(IPAddressBase):
#     id: int
#     subnet_id: int

#     class Config:
#         orm_mode = True

# # Update Subnet schema to include IP Addresses if needed (optional for now)
class Subnet(SubnetBase):
    id: int
    # ip_addresses: List[IPAddress] = [] # Example of including related data

    class Config:
        orm_mode = True

# IPAddress Schemas
class IPAddressBase(BaseModel):
    ip_address: str
    subnet_id: int
    status: Optional[str] = "Free"
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    notes: Optional[str] = None

class IPAddressCreate(IPAddressBase):
    pass

class IPAddressUpdate(BaseModel):
    ip_address: Optional[str] = None
    subnet_id: Optional[int] = None
    status: Optional[str] = None
    hostname: Optional[str] = None
    mac_address: Optional[str] = None
    notes: Optional[str] = None

class IPAddress(IPAddressBase):
    id: int
    # Optionally, include related subnet information
    # subnet: Optional[Subnet] = None # Assuming Subnet schema is defined

    class Config:
        orm_mode = True
