# Vehicle Allocation (Vallocation) Management Backend with FastAPI and MongoDB 


A fast and efficient **Vehicle Allocation System** built using **FastAPI** and **MongoDB**, designed to allow employees to allocate vehicles for specific dates, manage allocation statuses, and handle driver assignments. The system ensures that a vehicle is not double-booked and enforces date restrictions to prevent allocation modifications after the allocation date.

> [!NOTE]
> Please check the [official website](https://fahimfba.github.io/vallocation/) for the complete instructions along with some popular resources!

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Requirements](#requirements)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [API Endpoints](#api-endpoints)
  - [Create an Allocation](#create-an-allocation)
  - [Update an Allocation](#update-an-allocation)
  - [Delete an Allocation](#delete-an-allocation)
  - [Get Allocations](#get-allocations)
- [Database Schema](#database-schema)
- [Testing](#testing)
- [Contributors](#contributors)

## Overview

The **Vehicle Allocation System** is a RESTful API that allows employees to reserve vehicles for specific days. Each vehicle has an assigned driver, and only one vehicle can be allocated per employee for a given day. Additionally, users can view, update, and delete allocations, provided the actions are performed before the allocated date.

This project is designed to handle a high number of users and vehicles, with optimizations for load handling and database efficiency.

## Features

- **Create Allocations:** Employees can allocate vehicles for future dates.
- **Update Allocations:** Modify existing allocations before the allocation date.
- **Delete Allocations:** Cancel allocations before the allocation date.
- **Conflict Prevention:** Prevents multiple allocations of the same vehicle on the same date.
- **Status Tracking:** Tracks the status of each allocation (e.g., pending, confirmed, canceled).
- **Driver Assignment:** Each vehicle is pre-assigned to a driver.
- **Performance Optimized:** Handles a large number of concurrent users and operations.
  
## Tech Stack

- **Backend:** FastAPI
- **Database:** MongoDB (Async with Motor)
- **ORM:** Pydantic (For schema validation)
- **Environment Management:** Python virtual environment
- **Testing:** Pytest

## Requirements

- **Python 3.9+**
- **MongoDB**
- **FastAPI**
- **Pydantic**
- **Motor** (Async MongoDB driver)

## Installation

Follow these steps to set up and run the project locally.

### 1. Clone the repository
```bash
git clone https://github.com/FahimFBA/vallocation
cd vallocation
```

### 2. Create a virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: `env\Scripts\activate`
```

### 3. Install the required dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up environment variables
Create a `.env` file in the root directory with the following content:
```
MONGO_USERNAME=your_username
MONGO_PASSWORD=your_password
MONGO_CLUSTER_URL=your_mongodb_cluster_name
```

### 5. Run the application
Start the FastAPI server:
```bash
uvicorn main:app --reload
```
or,
```bash
fastapi dev main.py
```

The API will now be available at `http://127.0.0.1:8000`.

## Project Structure

```bash
vallocation/
│
├── config/
│   └── database.py        # Database configuration for MongoDB
│
├── docs/                  # Documentation (Docusaurus)
│
├── models/
│   └── vallocation_model.py   # Pydantic model for vehicle allocations
│
├── routers/
│   └── route.py           # FastAPI routes for vehicle allocation
│
├── schemas/
│   └── schemas.py         # Pydantic schemas for request/response models
│
├── .env.example           # Example environment variables file
├── .gitignore             # Git ignore rules
├── LICENSE                # License file for the project
├── main.py                # Entry point of the FastAPI application
├── requirements.txt       # Python dependencies for the project
```

## API Endpoints

### Create an Allocation
- **Endpoint:** `POST /allocate`
- **Description:** Allocates a vehicle for a given employee on a specified date.
- **Request Body:**
  ```json
  {
    "employee_id": 101,
    "vehicle_id": 456,
    "allocation_date": "2024-11-01"
  }
  ```
- **Response:**
  ```json
  {
    "id": "60c72b2f9b7e4e2d88d0f66b",
    "employee_id": 101,
    "vehicle_id": 456,
    "driver_id": 45,
    "allocation_date": "2024-11-01",
    "status": "pending"
  }
  ```

### Update an Allocation
- **Endpoint:** `PUT /allocate/{allocation_id}`
- **Description:** Updates an existing allocation (e.g., change date or status).
- **Request Body:**
  ```json
  {
    "allocation_date": "2024-11-02",
    "status": "confirmed"
  }
  ```

### Delete an Allocation
- **Endpoint:** `DELETE /allocate/{allocation_id}`
- **Description:** Deletes an allocation before the allocation date.
- **Response:**
  ```json
  {
    "message": "Allocation deleted successfully"
  }
  ```

### Get Allocations
- **Endpoint:** `GET /allocations`
- **Description:** Fetches all allocations for the current user.
- **Response:**
  ```json
  [
    {
      "id": "60c72b2f9b7e4e2d88d0f66b",
      "employee_id": 101,
      "vehicle_id": 456,
      "driver_id": 45,
      "allocation_date": "2024-11-01",
      "status": "pending"
    }
  ]
  ```

## Database Schema

Each allocation is stored in MongoDB in the following format:
```json
{
    "_id": "ObjectId('60c72b2f9b7e4e2d88d0f66b')",
    "employee_id": 101,
    "vehicle_id": 456,
    "driver_id": 45,
    "allocation_date": "2024-11-01",
    "status": "pending"
}
```

<!-- ## Testing

To run the test suite, execute the following command:
```bash
pytest
```

Ensure you have test data in your test database and properly mock external dependencies when running tests. -->

## Contributors

- **Fahim** - Developer, Architect
- **[Contributors](https://github.com/your-repo/contributors)**

Feel free to open issues or submit pull requests to help improve this project!

