"""
MongoDB Database Initialization Module

This module is responsible for initializing the MongoDB database connection,
creating necessary indexes, and setting up the database for the Vehicle Allocation System.
"""

from motor.motor_asyncio import AsyncIOMotorClient
from dotenv import load_dotenv
import os
import asyncio

# Load environment variables from .env file
load_dotenv()

# Retrieve the MongoDB credentials from the environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER_URL")

# Create the MongoDB connection URI using the loaded credentials
uri = f"mongodb+srv://{username}:{password}@{
    cluster}/?retryWrites=true&w=majority&appName=Cluster0"

# Initialize MongoDB client and access the database
client = AsyncIOMotorClient(uri)
db = client.vallocation_db
collection = db.vallocation_collection

# Function to create indexes
async def create_indexes():
    """
    Create necessary indexes in the MongoDB collection.

    Indexes:
    - Unique index on 'vehicle_id' and 'allocation_date' to prevent double booking
    - Index on 'employee_id' for efficient querying
    """
    await collection.create_index([("vehicle_id", 1), ("allocation_date", 1)], unique=True)
    await collection.create_index([("employee_id", 1)])

# Function to initialize the database at startup
async def initialize_db():
    """
    Initialize the MongoDB database by creating necessary indexes.
    """
    await create_indexes()

# For running it directly (testing purposes)
# if __name__ == "__main__":
#     asyncio.run(initialize_db())
