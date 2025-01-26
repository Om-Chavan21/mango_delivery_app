# app/schemas/customer_schema.py

from pydantic import BaseModel


class CustomerCreate(BaseModel):
    name: str
    phone_number: str
    address: str = None
    area_of_residence: str = None
    google_maps_link: str = None


class CustomerResponse(BaseModel):
    id: str
    name: str
    phone_number: str
    address: str = None
    area_of_residence: str = None
    google_maps_link: str = None


class CustomerUpdate(BaseModel):
    name: str = None
    phone_number: str = None
    address: str = None
    area_of_residence: str = None
    google_maps_link: str = None


class CustomerList(BaseModel):
    customers: list[CustomerResponse]
