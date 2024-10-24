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
    # Index on vehicle_id and allocation_date to prevent double booking
    await collection.create_index([("vehicle_id", 1), ("allocation_date", 1)], unique=True)
    await collection.create_index([("employee_id", 1)])  # Index on employee_id

# Function to initialize the database at startup
async def initialize_db():
    await create_indexes()

# For running it directly (testing purposes)
# if __name__ == "__main__":
#     asyncio.run(initialize_db())
