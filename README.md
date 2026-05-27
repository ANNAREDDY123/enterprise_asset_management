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
How to Run
Install dependencies:
pip install -r requirements.txt

Run the FastAPI server:
uvicorn main:app --reload

Open Swagger documentation in browser:
http://127.0.0.1:8000/docs

SQL Files
The sql folder contains:

schema.sql - database table creation script
report_queries.sql - SQL report queries
SQL Reports Included

Most assigned assets
Employees holding multiple assets
Monthly maintenance cost report
Assets not used for last 6 months
Asset utilization percentage
Department-wise asset allocation report
Top 5 expensive assets
Assets under maintenance with pending requests
Employee asset audit report using JOINs
Department ranking by asset value using Window Functions

Testing
Run tests using:
pytest

Explanation

I created this project using FastAPI and SQLAlchemy. The system manages users, employees, departments, assets, asset allocation, maintenance requests, and audit logs.

Authentication is handled using JWT tokens. Passwords are hashed before storing. Role-based access is added so Admin users can perform important actions like adding, updating, and deleting assets.

For asset management, I added APIs to add assets, update assets, view assets, and soft delete assets. Instead of permanently deleting an asset, I used soft delete by updating the is_deleted field and changing the asset status to Retired.

For asset allocation, I added APIs to assign assets to employees and return assets. Before assigning an asset, the system checks whether the asset is already assigned. This prevents duplicate asset assignment.

For maintenance management, I added APIs to raise maintenance requests and update maintenance status. When a maintenance request is raised, the asset status changes to Maintenance. When maintenance is completed, the asset can be changed back to Available.

I also added pagination, filtering, search APIs, audit logs, exception handling, Swagger documentation, SQL report queries, and a basic Pytest test file.

Submission
This repository contains:

FastAPI source code
SQL schema script
SQL report queries
README file
Pytest test file
Requirements file
