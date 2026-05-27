# Enterprise Asset Management System

## Objective
This project is a backend system to manage company assets, employees, asset allocation, maintenance tracking, and audit history.

## Tech Stack
- Python 3
- FastAPI
- SQLAlchemy
- Pydantic
- SQLite
- JWT Authentication
- Pytest

## Features
- User Register and Login
- JWT Token Authentication
- Role-Based Access
- Add, Update, View, and Soft Delete Assets
- Asset Status Tracking
- Employee Asset Allocation
- Asset Return
- Asset History
- Maintenance Request Management
- Maintenance Cost Tracking
- Search, Filtering, and Pagination
- Audit Logs
- Swagger Documentation
- Unit Testing with Pytest

## Project Structure
```text
enterprise_asset_management/
├── main.py
├── database.py
├── models.py
├── schemas.py
├── auth.py
├── requirements.txt
├── README.md
├── sql/
│   ├── schema.sql
│   └── report_queries.sql
└── tests/
    └── test_assets.py
