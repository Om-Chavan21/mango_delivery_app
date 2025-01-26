# app/main.py

from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from app.config import MONGODB_CONNECTION_URI, DB_NAME
from app.routers.customer_router import router as customer_router
from app.routers.product_router import router as product_router
from app.routers.order_router import router as order_router
from contextlib import asynccontextmanager

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize MongoDB client
    app.mongodb_client = AsyncIOMotorClient(MONGODB_CONNECTION_URI)
    app.database = app.mongodb_client[DB_NAME]
    print("Connected to MongoDB database!")

    yield  # This allows the application to run while connected

    # Clean up resources on shutdown
    app.mongodb_client.close()
    print("Disconnected from MongoDB database!")


app = FastAPI(lifespan=lifespan)

app.include_router(customer_router, prefix="/customers", tags=["customers"])
app.include_router(product_router, prefix="/products", tags=["products"])
app.include_router(order_router, prefix="/orders", tags=["orders"])


@app.get("/")
async def root():
    return {"message": "Welcome to the Mango Delivery API!"}
