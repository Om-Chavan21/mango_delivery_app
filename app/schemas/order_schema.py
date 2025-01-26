# app/schemas/order_schema.py

from pydantic import BaseModel
from typing import List
from datetime import datetime


class OrderedProductCreate(BaseModel):
    product_id: str  # Reference to Product ID
    quantity: int
    price: float


class OrderCreate(BaseModel):
    customer_id: str  # Reference to Customer ID
    ordered_products: List[
        OrderedProductCreate
    ]  # List of ordered products with quantity and price
    order_date: datetime = None  # Optional field for order date


class OrderResponse(BaseModel):
    id: str
    customer_id: str
    ordered_products: List[OrderedProductCreate]  # Include ordered products in response
    order_date: datetime  # Date of the order
    total_amount: float


class OrderUpdate(BaseModel):
    ordered_products: List[OrderedProductCreate] = None
    total_amount: float = None


class OrderList(BaseModel):
    orders: List[OrderResponse]
