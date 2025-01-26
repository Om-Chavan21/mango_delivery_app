# app/routers/order_router.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.models.order import Order as OrderModel
from app.schemas.order_schema import OrderCreate, OrderResponse, OrderUpdate, OrderList
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId
from datetime import datetime

router = APIRouter()


async def get_collection() -> AsyncIOMotorCollection:
    from app.main import app  # Importing app to access database connection

    return app.database["orders"]  # Accessing the database directly


@router.post("/", response_model=OrderResponse)
async def create_order(order_create: OrderCreate, collection=Depends(get_collection)):
    order_data = order_create.model_dump()  # Use model_dump instead of dict()

    # Calculate total amount based on ordered products
    total_amount = sum(
        item["price"] * item["quantity"] for item in order_data["ordered_products"]
    )

    order_data["total_amount"] = total_amount
    order_data["order_date"] = datetime.now()  # Set the current date and time

    result = await collection.insert_one(order_data)
    return {**order_data, "id": str(result.inserted_id)}


@router.get("/{order_id}", response_model=OrderResponse)
async def read_order(order_id: str, collection=Depends(get_collection)):
    order_data = await collection.find_one({"_id": ObjectId(order_id)})
    if order_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return {**order_data, "id": str(order_data["_id"])}


@router.put("/{order_id}", response_model=OrderResponse)
async def update_order(
    order_id: str, order_update: OrderUpdate, collection=Depends(get_collection)
):
    update_data = order_update.model_dump(
        exclude_unset=True
    )  # Use model_dump instead of dict()

    if "ordered_products" in update_data:
        total_amount = sum(
            item["price"] * item["quantity"] for item in update_data["ordered_products"]
        )
        update_data["total_amount"] = total_amount

    result = await collection.update_one(
        {"_id": ObjectId(order_id)}, {"$set": update_data}
    )

    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order not found or no changes made",
        )

    updated_order = await collection.find_one({"_id": ObjectId(order_id)})

    return {**updated_order, "id": str(updated_order["_id"])}


@router.delete("/{order_id}", response_model=dict)
async def delete_order(order_id: str, collection=Depends(get_collection)):
    result = await collection.delete_one({"_id": ObjectId(order_id)})

    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Order not found"
        )

    return {"message": "Order deleted successfully"}


@router.get("/", response_model=OrderList)
async def list_orders(collection=Depends(get_collection)):
    orders = []

    async for order in collection.find():
        orders.append({**order, "id": str(order["_id"])})

    return {"orders": orders}
