# app/schemas/product_schema.py

from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    description: str
    price: float
    stock_quantity: int


class ProductResponse(BaseModel):
    id: str
    name: str
    description: str
    price: float
    stock_quantity: int


class ProductUpdate(BaseModel):
    name: str = None
    description: str = None
    price: float = None
    stock_quantity: int = None


class ProductList(BaseModel):
    products: list[ProductResponse]
