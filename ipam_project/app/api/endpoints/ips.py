from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional

from ....app import crud, models, schemas # Adjusted import path
from ....app.database import get_db # Adjusted import path

router = APIRouter()

@router.post("/", response_model=schemas.IPAddress)
def create_ip_address_endpoint(ip_address: schemas.IPAddressCreate, db: Session = Depends(get_db)):
    # Check if IP address already exists
    existing_ip = db.query(models.IPAddress).filter(models.IPAddress.ip_address == ip_address.ip_address).first()
    if existing_ip:
        raise HTTPException(status_code=400, detail="IP address already exists")
    
    # Check if MAC address already exists (if provided)
    if ip_address.mac_address:
        existing_mac = db.query(models.IPAddress).filter(models.IPAddress.mac_address == ip_address.mac_address).first()
        if existing_mac:
            raise HTTPException(status_code=400, detail="MAC address already assigned to another IP")

    # CRUD function handles subnet existence check
    db_ip_address = crud.create_ipaddress(db=db, ipaddress=ip_address)
    if db_ip_address is None: # This means subnet was not found by CRUD function
        raise HTTPException(status_code=404, detail=f"Subnet with id {ip_address.subnet_id} not found")
    return db_ip_address

@router.get("/", response_model=List[schemas.IPAddress])
def read_ip_addresses_endpoint(
    subnet_id: Optional[int] = None,
    status: Optional[str] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    ip_addresses = crud.get_ipaddresses(db, subnet_id=subnet_id, status=status, skip=skip, limit=limit)
    return ip_addresses

@router.get("/{ip_id}", response_model=schemas.IPAddress)
def read_ip_address_endpoint(ip_id: int, db: Session = Depends(get_db)):
    db_ip_address = crud.get_ipaddress(db, ip_id=ip_id)
    if db_ip_address is None:
        raise HTTPException(status_code=404, detail="IP Address not found")
    return db_ip_address

@router.put("/{ip_id}", response_model=schemas.IPAddress)
def update_ip_address_endpoint(ip_id: int, ip_address_update: schemas.IPAddressUpdate, db: Session = Depends(get_db)):
    # Check if IP address exists
    db_ip_address = crud.get_ipaddress(db, ip_id=ip_id)
    if db_ip_address is None:
        raise HTTPException(status_code=404, detail="IP Address not found")

    # If IP address string is being updated, check for uniqueness
    if ip_address_update.ip_address and ip_address_update.ip_address != db_ip_address.ip_address:
        existing_ip = db.query(models.IPAddress).filter(models.IPAddress.ip_address == ip_address_update.ip_address).first()
        if existing_ip:
            raise HTTPException(status_code=400, detail="IP address already exists")

    # If MAC address is being updated, check for uniqueness
    if ip_address_update.mac_address and ip_address_update.mac_address != db_ip_address.mac_address:
        existing_mac = db.query(models.IPAddress).filter(models.IPAddress.mac_address == ip_address_update.mac_address).first()
        if existing_mac:
            raise HTTPException(status_code=400, detail="MAC address already assigned to another IP")
            
    updated_ip = crud.update_ipaddress(db=db, ip_id=ip_id, ipaddress_update=ip_address_update)
    
    if updated_ip == "SUBNET_NOT_FOUND":
        raise HTTPException(status_code=404, detail=f"Subnet with id {ip_address_update.subnet_id} not found for updating IP address")
    
    if updated_ip is None: # Should not happen if initial check passed, but good for safety
        raise HTTPException(status_code=404, detail="IP Address not found after update attempt")

    return updated_ip

@router.delete("/{ip_id}", response_model=schemas.IPAddress) # Or a message like {"message": "IP Address deleted"}
def delete_ip_address_endpoint(ip_id: int, db: Session = Depends(get_db)):
    db_ip_address = crud.get_ipaddress(db, ip_id=ip_id)
    if db_ip_address is None:
        raise HTTPException(status_code=404, detail="IP Address not found")
    
    deleted_ip = crud.delete_ipaddress(db=db, ip_id=ip_id)
    if deleted_ip is None: # Should be redundant given the check above
        raise HTTPException(status_code=404, detail="IP Address not found during deletion")
    return deleted_ip # Returns the deleted IP address object
