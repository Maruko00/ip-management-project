from sqlalchemy.orm import Session
from . import models, schemas

# Subnet CRUD operations
def get_subnet(db: Session, subnet_id: int):
    return db.query(models.Subnet).filter(models.Subnet.id == subnet_id).first()

def get_subnets(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Subnet).offset(skip).limit(limit).all()

def create_subnet(db: Session, subnet: schemas.SubnetCreate):
    db_subnet = models.Subnet(
        network_address=subnet.network_address,
        description=subnet.description,
        parent_subnet_id=subnet.parent_subnet_id
    )
    db.add(db_subnet)
    db.commit()
    db.refresh(db_subnet)
    return db_subnet

def update_subnet(db: Session, subnet_id: int, subnet_update: schemas.SubnetUpdate):
    db_subnet = get_subnet(db, subnet_id)
    if db_subnet:
        update_data = subnet_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_subnet, key, value)
        db.commit()
        db.refresh(db_subnet)
    return db_subnet

def delete_subnet(db: Session, subnet_id: int):
    """
    Deletes a subnet.
    Consideration: This is a basic delete. In a real-world scenario,
    one would need to decide how to handle IP addresses within this subnet
    (e.g., delete them, reassign them, or prevent deletion if IPs exist).
    """
    db_subnet = get_subnet(db, subnet_id)
    if db_subnet:
        db.delete(db_subnet)
        db.commit()
    return db_subnet

# IPAddress CRUD operations (to be defined later)
# def get_ip_address(db: Session, ip_address_id: int):
#     return db.query(models.IPAddress).filter(models.IPAddress.id == ip_address_id).first()

# def get_ip_addresses_by_subnet(db: Session, subnet_id: int, skip: int = 0, limit: int = 100):
#     return db.query(models.IPAddress).filter(models.IPAddress.subnet_id == subnet_id).offset(skip).limit(limit).all()

# def create_ip_address(db: Session, ip_address: schemas.IPAddressCreate):
#     db_ip_address = models.IPAddress(**ip_address.model_dump())
#     db.add(db_ip_address)
#     db.commit()
#     db.refresh(db_ip_address)
#     return db_ip_address

def get_ipaddress(db: Session, ip_id: int):
    return db.query(models.IPAddress).filter(models.IPAddress.id == ip_id).first()

def get_ipaddresses(db: Session, subnet_id: Optional[int] = None, status: Optional[str] = None, skip: int = 0, limit: int = 100):
    query = db.query(models.IPAddress)
    if subnet_id is not None:
        query = query.filter(models.IPAddress.subnet_id == subnet_id)
    if status is not None:
        query = query.filter(models.IPAddress.status == status)
    return query.offset(skip).limit(limit).all()

def create_ipaddress(db: Session, ipaddress: schemas.IPAddressCreate):
    # Check if the subnet exists
    db_subnet = get_subnet(db, subnet_id=ipaddress.subnet_id)
    if not db_subnet:
        return None # Indicate subnet not found, will be handled in endpoint
    db_ipaddress = models.IPAddress(**ipaddress.model_dump())
    db.add(db_ipaddress)
    db.commit()
    db.refresh(db_ipaddress)
    return db_ipaddress

def update_ipaddress(db: Session, ip_id: int, ipaddress_update: schemas.IPAddressUpdate):
    db_ipaddress = get_ipaddress(db, ip_id)
    if db_ipaddress:
        if ipaddress_update.subnet_id is not None:
            # Check if the new subnet exists
            db_subnet = get_subnet(db, subnet_id=ipaddress_update.subnet_id)
            if not db_subnet:
                return "SUBNET_NOT_FOUND" # Special marker for endpoint to handle
        
        update_data = ipaddress_update.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_ipaddress, key, value)
        db.commit()
        db.refresh(db_ipaddress)
    return db_ipaddress

def delete_ipaddress(db: Session, ip_id: int):
    db_ipaddress = get_ipaddress(db, ip_id)
    if db_ipaddress:
        db.delete(db_ipaddress)
        db.commit()
    return db_ipaddress
