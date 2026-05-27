from sqlalchemy import Column, Integer, String, Float, Boolean, Date, DateTime, ForeignKey, Text
from datetime import datetime
from database import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

class Department(Base):
    __tablename__ = "departments"

    department_id = Column(Integer, primary_key=True, index=True)
    department_name = Column(String(100), nullable=False)

class Employee(Base):
    __tablename__ = "employees"

    employee_id = Column(Integer, primary_key=True, index=True)
    employee_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True)
    department_id = Column(Integer, ForeignKey("departments.department_id"))

class Asset(Base):
    __tablename__ = "assets"

    asset_id = Column(Integer, primary_key=True, index=True)
    asset_name = Column(String(100), nullable=False)
    asset_type = Column(String(100))
    serial_number = Column(String(100), unique=True)
    purchase_cost = Column(Float)
    status = Column(String(50), default="Available")
    is_deleted = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class AssetAllocation(Base):
    __tablename__ = "asset_allocations"

    allocation_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    employee_id = Column(Integer, ForeignKey("employees.employee_id"))
    assigned_date = Column(Date)
    return_date = Column(Date, nullable=True)
    status = Column(String(50), default="Assigned")

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    request_id = Column(Integer, primary_key=True, index=True)
    asset_id = Column(Integer, ForeignKey("assets.asset_id"))
    issue_description = Column(Text)
    maintenance_status = Column(String(50), default="Pending")
    cost = Column(Float, default=0)
    request_date = Column(DateTime, default=datetime.utcnow)

class AuditLog(Base):
    __tablename__ = "audit_logs"

    audit_id = Column(Integer, primary_key=True, index=True)
    action = Column(String(100))
    table_name = Column(String(100))
    record_id = Column(Integer)
    performed_by = Column(String(100))
    action_time = Column(DateTime, default=datetime.utcnow)
