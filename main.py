"""
Vehicle Allocation System API

This API is designed to manage vehicle allocations for employees.
It includes CRUD operations and history reporting.
"""

from fastapi import FastAPI
from routers import route
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI(
    title="Vehicle Allocation System",
    description="API for managing vehicle allocations for employees. "
                "Includes CRUD operations and history reporting.",
    version="1.0.0",
)

# Include the router from route.py
app.include_router(route.router)

"""
Set up CORS (for future feat. integration: frontend or external access)
"""
origins = [
    "http://localhost",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health Check endpoint
@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "healthy"}


# Main entry point when running the app directly
if __name__ == "__main__":
    """
    Run the FastAPI application using the uvicorn server.

    Host: Binds the server to all available network interfaces.
    Port: Runs the server on port 8000.
    Reload: Automatically reloads the server when code changes are detected.
    """
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
