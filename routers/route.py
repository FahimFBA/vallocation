"""
FastAPI router for vehicle allocation management.

This router provides APIs for creating, updating, deleting, and retrieving vehicle allocations.
It also includes helper functions for data validation and querying the MongoDB database.
"""

from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List, Optional, Dict, Any
from motor.motor_asyncio import AsyncIOMotorCollection
from datetime import date, datetime
from bson import ObjectId
from models.vallocation_model import Vallocation
from schemas.schemas import VallocationCreate, VallocationUpdate, VallocationResponse
from config.database import collection

router = APIRouter()

# Helper function to check if a vehicle is already allocated for a specific day
async def is_vehicle_allocated(vehicle_id: int, allocation_date: date, collection: AsyncIOMotorCollection) -> bool:
    """
    Check if a vehicle is already allocated for a specific date.

    Args:
        vehicle_id (int): The ID of the vehicle.
        allocation_date (date): The allocation date to check.
        collection (AsyncIOMotorCollection): The MongoDB collection.

    Returns:
        bool: True if the vehicle is already allocated for the given date, False otherwise.
    """
    existing_allocation = await collection.find_one({
        "vehicle_id": vehicle_id,
        "allocation_date": allocation_date.isoformat()
    })
    return existing_allocation is not None

# Helper function to validate if allocation date is before today
def is_date_in_future(allocation_date: date) -> bool:
    """
    Check if an allocation date is in the future.

    Args:
        allocation_date (date): The allocation date to check.

    Returns:
        bool: True if the allocation date is in the future, False otherwise.
    """
    return allocation_date >= date.today()

# Create an allocation
@router.post("/allocate/", response_model=VallocationResponse, summary="Create a new vehicle allocation")
async def create_allocation(allocation: VallocationCreate, collection: AsyncIOMotorCollection = Depends(lambda: collection)):
    """
    Create a new vehicle allocation.

    Args:
        allocation (VallocationCreate): The allocation data to create.
        collection (AsyncIOMotorCollection): The MongoDB collection (provided as a dependency).

    Raises:
        HTTPException: If the allocation date is not in the future or the vehicle is already allocated for the requested date.

    Returns:
        VallocationResponse: The created allocation data.
    """
    # Check if the allocation date is in the future
    if not is_date_in_future(allocation.allocation_date):
        raise HTTPException(
            status_code=400, detail="Allocation date must be in the future."
        )

    # Check if the vehicle is already allocated for the requested date
    if await is_vehicle_allocated(allocation.vehicle_id, allocation.allocation_date, collection):
        raise HTTPException(
            status_code=400, detail="Vehicle is already allocated for the requested date."
        )

    # Get pre-assigned driver for the vehicle (for simplicity, driver_id is set same as vehicle_id here)
    driver_id = allocation.vehicle_id

    # Insert new allocation into MongoDB
    new_allocation = {
        "employee_id": allocation.employee_id,
        "vehicle_id": allocation.vehicle_id,
        "driver_id": driver_id,
        "allocation_date": allocation.allocation_date.isoformat(),
        "status": "pending",
    }
    result = await collection.insert_one(new_allocation)

    # Return the created allocation
    created_allocation = await collection.find_one({"_id": result.inserted_id})
    return VallocationResponse(id=str(created_allocation["_id"]), **created_allocation)

# Update an allocation
@router.put("/allocate/{allocation_id}", response_model=VallocationResponse, summary="Update an existing vehicle allocation")
async def update_allocation(allocation_id: str, allocation: VallocationUpdate, collection: AsyncIOMotorCollection = Depends(lambda: collection)):
    """
    Update an existing vehicle allocation.

    Args:
        allocation_id (str): The ID of the allocation to update.
        allocation (VallocationUpdate): The updated allocation data.
        collection (AsyncIOMotorCollection): The MongoDB collection (provided as a dependency).

    Raises:
        HTTPException: If the allocation ID is invalid, the allocation does not exist, the allocation date is not in the future,
            or the vehicle is already allocated for the new requested date.

    Returns:
        VallocationResponse: The updated allocation data.
    """
    # Check if the allocation exists
    try:
        existing_allocation = await collection.find_one({"_id": ObjectId(allocation_id)})
    except Exception:
        raise HTTPException(
            status_code=400, detail="Invalid allocation ID format.")

    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found.")

    # Ensure the allocation date is in the future for modifications
    existing_allocation_date = datetime.strptime(
        existing_allocation["allocation_date"], "%Y-%m-%d").date()
    if not is_date_in_future(existing_allocation_date):
        raise HTTPException(
            status_code=400, detail="Cannot update allocations that have already passed."
        )

    # If updating allocation date, ensure the vehicle is not already allocated for the new date
    if allocation.allocation_date:
        allocation_date_obj = allocation.allocation_date
        if await is_vehicle_allocated(existing_allocation["vehicle_id"], allocation_date_obj, collection):
            raise HTTPException(
                status_code=400, detail="Vehicle is already allocated for the new requested date."
            )

    # Update the allocation fields
    update_data = {k: v for k, v in allocation.dict(
        exclude_unset=True).items()}

    # Handle date formatting if allocation_date is being updated
    if 'allocation_date' in update_data:
        update_data['allocation_date'] = allocation.allocation_date.isoformat()

    # Perform the update in MongoDB
    await collection.update_one({"_id": ObjectId(allocation_id)}, {"$set": update_data})

    # Return the updated allocation
    updated_allocation = await collection.find_one({"_id": ObjectId(allocation_id)})

    return VallocationResponse(id=str(updated_allocation["_id"]), **updated_allocation)

# Delete an allocation
@router.delete("/allocate/{allocation_id}", summary="Delete an existing vehicle allocation")
async def delete_allocation(allocation_id: str, collection: AsyncIOMotorCollection = Depends(lambda: collection)):
    """
    Delete an existing vehicle allocation.

    Args:
        allocation_id (str): The ID of the allocation to delete.
        collection (AsyncIOMotorCollection): The MongoDB collection (provided as a dependency).

    Raises:
        HTTPException: If the allocation does not exist or the allocation date is not in the future.

    Returns:
        dict: A success message.
    """
    # Check if the allocation exists
    existing_allocation = await collection.find_one({"_id": ObjectId(allocation_id)})
    if not existing_allocation:
        raise HTTPException(status_code=404, detail="Allocation not found.")

    # Ensure the allocation date is in the future for deletions
    existing_allocation_date = datetime.strptime(
        existing_allocation["allocation_date"], "%Y-%m-%d").date()
    if not is_date_in_future(existing_allocation_date):
        raise HTTPException(
            status_code=400, detail="Cannot delete allocations that have already passed."
        )

    # Delete the allocation
    await collection.delete_one({"_id": ObjectId(allocation_id)})
    return {"detail": "Allocation deleted successfully."}

# Get allocation history with pagination and filters
@router.get("/history/", response_model=Dict[str, Any], summary="Get allocation history with optional filters and pagination")
async def get_allocation_history(
    employee_id: Optional[int] = None,
    vehicle_id: Optional[int] = None,
    driver_id: Optional[int] = None,
    allocation_date: Optional[date] = None,
    skip: int = Query(0, description="Number of records to skip"),
    limit: int = Query(10, description="Max number of records to return"),
    collection: AsyncIOMotorCollection = Depends(lambda: collection)
):
    """
    Get allocation history with optional filters and pagination.

    Args:
        employee_id (Optional[int], optional): Filter allocations by employee ID.
        vehicle_id (Optional[int], optional): Filter allocations by vehicle ID.
        driver_id (Optional[int], optional): Filter allocations by driver ID.
        allocation_date (Optional[date], optional): Filter allocations by allocation date.
        skip (int, optional): The number of records to skip. Defaults to 0.
        limit (int, optional): The maximum number of records to return. Defaults to 10.
        collection (AsyncIOMotorCollection): The MongoDB collection (provided as a dependency).

    Returns:
        Dict[str, Any]: The filtered allocation history with pagination metadata.
    """
    # Build the filter query
    query = {}
    if employee_id is not None:
        query["employee_id"] = employee_id
    if vehicle_id is not None:
        query["vehicle_id"] = vehicle_id
    if driver_id is not None:
        query["driver_id"] = driver_id
    if allocation_date is not None:
        query["allocation_date"] = allocation_date.isoformat()

    # Query the database for matching allocations with skip and limit
    allocations = await collection.find(query).skip(skip).limit(limit).to_list(length=limit)

    # Get total count of allocations
    total_count = await collection.count_documents(query)

    # Return the filtered allocation history and pagination metadata
    return {
        "total": total_count,
        "skip": skip,
        "limit": limit,
        "results": [VallocationResponse(id=str(allocation["_id"]), **allocation) for allocation in allocations]
    }
