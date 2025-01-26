# app/models/customer.py

from bson import ObjectId
from pydantic import BaseModel, Field


class Customer(BaseModel):
    id: str = Field(
        default_factory=lambda: str(ObjectId()), alias="_id"
    )  # MongoDB ObjectId
    name: str
    phone_number: str
    address: str = None
    area_of_residence: str = None
    google_maps_link: str = None

    class Config:
        allow_population_by_field_name = True  # Allows using _id as id
