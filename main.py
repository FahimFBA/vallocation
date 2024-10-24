import os
from dotenv import load_dotenv
from pymongo.server_api import ServerApi
from pymongo.mongo_client import MongoClient
from fastapi import FastAPI

app = FastAPI()


# Load environment variables from .env file
load_dotenv()

# Retrieve the MongoDB credentials from the environment variables
username = os.getenv("MONGO_USERNAME")
password = os.getenv("MONGO_PASSWORD")
cluster = os.getenv("MONGO_CLUSTER_URL")

# Create the MongoDB connection URI using the loaded credentials
uri = f"mongodb+srv://{username}:{password}@{
    cluster}/?retryWrites=true&w=majority&appName=Cluster0"


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))

# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)
