# app/routers/customer_router.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.models.customer import Customer as CustomerModel
from app.schemas.customer_schema import (
    CustomerCreate,
    CustomerResponse,
    CustomerUpdate,
    CustomerList,
)
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

router = APIRouter()


async def get_collection() -> AsyncIOMotorCollection:
    from app.main import app  # Importing app to access database connection

    return app.database["customers"]  # Accessing the database directly


@router.post("/", response_model=CustomerResponse)
async def create_customer(
    customer_create: CustomerCreate, collection=Depends(get_collection)
):
    customer_data = customer_create.dict()
    result = await collection.insert_one(customer_data)
    return {**customer_data, "id": str(result.inserted_id)}


@router.get("/{customer_id}", response_model=CustomerResponse)
async def read_customer(customer_id: str, collection=Depends(get_collection)):
    customer_data = await collection.find_one({"_id": ObjectId(customer_id)})
    if customer_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return {**customer_data, "id": str(customer_data["_id"])}


@router.put("/{customer_id}", response_model=CustomerResponse)
async def update_customer(
    customer_id: str,
    customer_update: CustomerUpdate,
    collection=Depends(get_collection),
):
    update_data = customer_update.dict(exclude_unset=True)
    result = await collection.update_one(
        {"_id": ObjectId(customer_id)}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Customer not found or no changes made",
        )
    updated_customer = await collection.find_one({"_id": ObjectId(customer_id)})
    return {**updated_customer, "id": str(updated_customer["_id"])}


@router.delete("/{customer_id}", response_model=dict)
async def delete_customer(customer_id: str, collection=Depends(get_collection)):
    result = await collection.delete_one({"_id": ObjectId(customer_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Customer not found"
        )
    return {"message": "Customer deleted successfully"}


@router.get("/", response_model=CustomerList)
async def list_customers(collection=Depends(get_collection)):
    customers = []
    async for customer in collection.find():
        customers.append({**customer, "id": str(customer["_id"])})
    return {"customers": customers}
