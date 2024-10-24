"""
Pydantic models for creating, updating, and responding with vehicle allocation data.
"""

from pydantic import BaseModel, Field
from datetime import date
from typing import Optional


class VallocationCreate(BaseModel):
    """
    Pydantic model for creating a new vehicle allocation.

    Attributes:
        employee_id (int): ID of the employee allocating the vehicle.
        vehicle_id (int): ID of the allocated vehicle.
        allocation_date (date): The date for which the vehicle is allocated.
    """
    employee_id: int = Field(...,
                             description="ID of the employee allocating the vehicle")
    vehicle_id: int = Field(..., description="ID of the allocated vehicle")
    allocation_date: date = Field(...,
                                  description="The date for which the vehicle is allocated")

    class Config:
        """
        Pydantic configuration for the VallocationCreate model.

        Includes an example JSON schema for documentation purposes.
        """
        json_schema_extra = {
            "example": {
                "employee_id": 101,
                "vehicle_id": 12,
                "allocation_date": "2024-11-01"
            }
        }


class VallocationUpdate(BaseModel):
    """
    Pydantic model for updating an existing vehicle allocation.

    Attributes:
        allocation_date (date, optional): Updated allocation date.
        status (str, optional): Status of the allocation (e.g., pending, confirmed, canceled).
    """
    allocation_date: Optional[date] = Field(
        None, description="Updated allocation date")
    status: Optional[str] = Field(
        None, description="Status of the allocation (e.g., pending, confirmed, canceled)")

    class Config:
        """
        Pydantic configuration for the VallocationUpdate model.

        Includes an example JSON schema for documentation purposes.
        """
        json_schema_extra = {
            "example": {
                "allocation_date": "2024-11-02",
                "status": "confirmed"
            }
        }


class VallocationResponse(BaseModel):
    """
    Pydantic model for representing a vehicle allocation response.

    Attributes:
        id (str): Unique ID of the allocation.
        employee_id (int): ID of the employee who allocated the vehicle.
        vehicle_id (int): ID of the allocated vehicle.
        driver_id (int): ID of the driver assigned to the vehicle.
        allocation_date (date): The date for which the vehicle is allocated.
        status (str): Status of the allocation (e.g., pending, confirmed, canceled).
    """
    id: str = Field(..., description="Unique ID of the allocation")
    employee_id: int = Field(...,
                             description="ID of the employee who allocated the vehicle")
    vehicle_id: int = Field(..., description="ID of the allocated vehicle")
    driver_id: int = Field(...,
                           description="ID of the driver assigned to the vehicle")
    allocation_date: date = Field(...,
                                  description="The date for which the vehicle is allocated")
    status: str = Field(
        ..., description="Status of the allocation (e.g., pending, confirmed, canceled)")

    class Config:
        """
        Pydantic configuration for the VallocationResponse model.

        Includes an example JSON schema for documentation purposes.
        """
        json_schema_extra = {
            "example": {
                "id": "60c72b2f9b7e4e2d88d0f66b",
                "employee_id": 101,
                "vehicle_id": 12,
                "driver_id": 45,
                "allocation_date": "2024-11-01",
                "status": "pending"
            }
        }
