# app/config.py

import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

MONGODB_CONNECTION_URI = os.getenv("MONGODB_CONNECTION_URI")
DB_NAME = os.getenv("DB_NAME")
