# app/models/order.py

from bson import ObjectId
from pydantic import BaseModel, Field
from typing import List
from datetime import datetime


class OrderedProduct(BaseModel):
    product_id: str  # Reference to Product ID
    quantity: int
    price: float


class Order(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ObjectId()), alias="_id"
    )  # MongoDB ObjectId
    customer_id: str  # Reference to Customer ID
    ordered_products: List[
        OrderedProduct
    ]  # List of ordered products with quantity and price
    order_date: datetime = Field(default_factory=datetime.utcnow)  # Date of the order
    total_amount: float

    class Config:
        allow_population_by_field_name = True  # Allows using _id as id
