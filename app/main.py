from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import dotenv_values
from contextlib import asynccontextmanager

config = dotenv_values(".env")

app = FastAPI()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Load the MongoDB client
    app.mongodb_client = AsyncIOMotorClient(config["MONGODB_CONNECTION_URI"])
    app.database = app.mongodb_client[config["DB_NAME"]]
    print("Connected to MongoDB database!")

    yield  # This will allow the application to run while connected

    # Clean up resources on shutdown
    app.mongodb_client.close()
    print("Disconnected from MongoDB database!")


# Pass the lifespan context manager to FastAPI
app = FastAPI(lifespan=lifespan)


@app.get("/")
async def root():
    return {"message": "Welcome to the Mango Delivery API!"}
