from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ....app import crud, models, schemas # Adjusted import path
from ....app.database import get_db # Adjusted import path

router = APIRouter()

@router.post("/", response_model=schemas.Subnet)
def create_subnet_endpoint(subnet: schemas.SubnetCreate, db: Session = Depends(get_db)):
    # Check if subnet with the same network address already exists
    # db_subnet = db.query(models.Subnet).filter(models.Subnet.network_address == subnet.network_address).first()
    # if db_subnet:
    #     raise HTTPException(status_code=400, detail="Subnet with this network address already exists")
    return crud.create_subnet(db=db, subnet=subnet)

@router.get("/", response_model=List[schemas.Subnet])
def read_subnets_endpoint(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    subnets = crud.get_subnets(db, skip=skip, limit=limit)
    return subnets

@router.get("/{subnet_id}", response_model=schemas.Subnet)
def read_subnet_endpoint(subnet_id: int, db: Session = Depends(get_db)):
    db_subnet = crud.get_subnet(db, subnet_id=subnet_id)
    if db_subnet is None:
        raise HTTPException(status_code=404, detail="Subnet not found")
    return db_subnet

@router.put("/{subnet_id}", response_model=schemas.Subnet)
def update_subnet_endpoint(subnet_id: int, subnet_update: schemas.SubnetUpdate, db: Session = Depends(get_db)):
    db_subnet = crud.get_subnet(db, subnet_id=subnet_id)
    if db_subnet is None:
        raise HTTPException(status_code=404, detail="Subnet not found")
    # Optionally, check for network_address conflicts if it's being updated
    # if subnet_update.network_address:
    #     existing_subnet = db.query(models.Subnet).filter(models.Subnet.network_address == subnet_update.network_address, models.Subnet.id != subnet_id).first()
    #     if existing_subnet:
    #         raise HTTPException(status_code=400, detail="Another subnet with this network address already exists")
    return crud.update_subnet(db=db, subnet_id=subnet_id, subnet_update=subnet_update)

@router.delete("/{subnet_id}", response_model=schemas.Subnet) # Or return a message e.g. status_code=204
def delete_subnet_endpoint(subnet_id: int, db: Session = Depends(get_db)):
    db_subnet = crud.get_subnet(db, subnet_id=subnet_id)
    if db_subnet is None:
        raise HTTPException(status_code=404, detail="Subnet not found")
    # Add logic here to handle child subnets or IPs if necessary before deletion
    # For example, prevent deletion if there are active IPs or child subnets
    # if db.query(models.IPAddress).filter(models.IPAddress.subnet_id == subnet_id).first():
    #     raise HTTPException(status_code=400, detail="Cannot delete subnet with active IP addresses")
    # if db.query(models.Subnet).filter(models.Subnet.parent_subnet_id == subnet_id).first():
    #     raise HTTPException(status_code=400, detail="Cannot delete subnet with child subnets")
    deleted_subnet = crud.delete_subnet(db=db, subnet_id=subnet_id)
    return deleted_subnet # Returning the deleted object; can also return a message like {"message": "Subnet deleted"}
