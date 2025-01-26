# app/routers/product_router.py

from fastapi import APIRouter, HTTPException, Depends, status
from app.models.product import Product as ProductModel
from app.schemas.product_schema import (
    ProductCreate,
    ProductResponse,
    ProductUpdate,
    ProductList,
)
from motor.motor_asyncio import AsyncIOMotorCollection
from bson import ObjectId

router = APIRouter()


async def get_collection() -> AsyncIOMotorCollection:
    from app.main import app  # Importing app to access database connection

    return app.database["products"]  # Accessing the database directly


@router.post("/", response_model=ProductResponse)
async def create_product(
    product_create: ProductCreate, collection=Depends(get_collection)
):
    product_data = product_create.dict()
    result = await collection.insert_one(product_data)
    return {**product_data, "id": str(result.inserted_id)}


@router.get("/{product_id}", response_model=ProductResponse)
async def read_product(product_id: str, collection=Depends(get_collection)):
    product_data = await collection.find_one({"_id": ObjectId(product_id)})
    if product_data is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return {**product_data, "id": str(product_data["_id"])}


@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str, product_update: ProductUpdate, collection=Depends(get_collection)
):
    update_data = product_update.dict(exclude_unset=True)
    result = await collection.update_one(
        {"_id": ObjectId(product_id)}, {"$set": update_data}
    )
    if result.modified_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found or no changes made",
        )
    updated_product = await collection.find_one({"_id": ObjectId(product_id)})
    return {**updated_product, "id": str(updated_product["_id"])}


@router.delete("/{product_id}", response_model=dict)
async def delete_product(product_id: str, collection=Depends(get_collection)):
    result = await collection.delete_one({"_id": ObjectId(product_id)})
    if result.deleted_count == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
    return {"message": "Product deleted successfully"}


@router.get("/", response_model=ProductList)
async def list_products(collection=Depends(get_collection)):
    products = []
    async for product in collection.find():
        products.append({**product, "id": str(product["_id"])})
    return {"products": products}
