from fastapi import FastAPI
from .database import create_db_and_tables
from .api.endpoints import subnets as subnet_router
from .api.endpoints import ips as ip_router # Import the IP address router

app = FastAPI()

@app.on_event("startup")
async def on_startup():
    create_db_and_tables()

app.include_router(subnet_router.router, prefix="/subnets", tags=["subnets"])
app.include_router(ip_router.router, prefix="/ips", tags=["ip_addresses"]) # Include the IP address router

@app.get("/")
async def root():
    return {"message": "Welcome to IPAM API"}
