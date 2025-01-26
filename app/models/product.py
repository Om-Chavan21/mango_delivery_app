# app/models/product.py

from pydantic import BaseModel, Field
from bson import ObjectId


class Product(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ObjectId()), alias="_id"
    )  # MongoDB ObjectId
    name: str
    description: str
    price: float
    stock_quantity: int

    class Config:
        allow_population_by_field_name = True  # Allows using _id as id
