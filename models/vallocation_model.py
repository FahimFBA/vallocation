"""
Pydantic models for the Vehicle Allocation System API.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class Vallocation(BaseModel):
    """
    Pydantic model representing a vehicle allocation.

    Attributes:
        employee_id (int): ID of the employee allocating the vehicle.
        vehicle_id (int): ID of the allocated vehicle.
        driver_id (int): ID of the driver assigned to the vehicle.
        allocation_date (date): The date for which the vehicle is allocated.
        status (str, optional): Status of the allocation (e.g., pending, confirmed, canceled). Defaults to "pending".
    """
    employee_id: int = Field(...,
                             description="ID of the employee allocating the vehicle")
    vehicle_id: int = Field(..., description="ID of the allocated vehicle")
    driver_id: int = Field(...,
                           description="ID of the driver assigned to the vehicle")
    allocation_date: date = Field(...,
                                  description="The date for which the vehicle is allocated")
    status: Optional[str] = Field(
        "pending", description="Status of the allocation (e.g., pending, confirmed, canceled)")

    class Config:
        """
        Pydantic configuration for the Vallocation model.

        Includes an example JSON schema for documentation purposes.
        """
        json_schema_extra = {
            "example": {
                "employee_id": 123,
                "vehicle_id": 456,
                "allocation_date": "2024-10-31",
                "status": "pending"
            }
        }
