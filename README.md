# FastAPI Practical Assessment 2 — Campus Lost & Found + Event Reservation APIs

## Description
Two FastAPI applications built for a B.Tech CSE-AI practical assessment:
1. **Task 1** — Campus Lost & Found API
2. **Task 2** — Campus Event Seat Reservation API

## Features
- Full CRUD operations using FastAPI + SQLModel
- SQLite database with automatic table creation
- Field validation using Pydantic
- Business logic: seat capacity enforcement, event status checks
- Interactive testing via Swagger UI

## Technologies Used
- FastAPI
- SQLModel / Pydantic
- SQLite
- Uvicorn
- Python 3.13

## Project Structure

CRC Training - Backend (FastAPI)_Practical Assessment/
├── task1/ (Lost & Found API)
├── task2/ (Event Reservation API)
├── screenshots/ (Testing evidence)
├── requirements.txt
└── README.md


## Installation
```powershell
git clone <your-repo-url>
cd "CRC Training - Backend (FastAPI)_Practical Assessment"
python -m venv venv
.\venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Running Task 1
```powershell
cd task1
uvicorn main:app --reload --port 8001
```
Swagger UI: http://127.0.0.1:8001/docs

## Running Task 2
```powershell
cd task2
uvicorn main:app --reload --port 8002
```
Swagger UI: http://127.0.0.1:8002/docs

## Task 1 Endpoints
- POST /items
- GET /items
- GET /items/{item_id}
- PUT /items/{item_id}
- DELETE /items/{item_id}
- GET /items/status/{status}
- GET /items/category/{category}

## Task 2 Endpoints
- POST /events, GET /events, GET/PUT/DELETE /events/{event_id}
- POST /events/{event_id}/reserve
- GET /events/{event_id}/reservations
- DELETE /reservations/{reservation_id}
- GET /events/{event_id}/availability

## Database
Each task uses its own SQLite file (`lostfound.db`, `events.db`), created automatically on startup via `create_engine()` and `SQLModel.metadata.create_all()`.

## Validation & Business Logic
- Item status restricted to Lost/Found/Returned
- Event status restricted to Open/Closed, capacity must be > 0
- Reservations blocked if event is closed, full, or doesn't exist
- Email validated using Pydantic's EmailStr

## Testing
All endpoints tested manually via Swagger UI (`/docs`). See `screenshots/` folder for evidence of successful and error responses.

## Screenshots
See `screenshots/` folder — includes CRUD operations, filtering, validation errors, 404 handling, and overbooking rejection. 