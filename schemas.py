from pydantic import BaseModel, Field
from typing import Optional
from datetime import date

class UserRegister(BaseModel):
    username: str = Field(min_length=3)
    password: str = Field(min_length=6)
    role: str

class UserLogin(BaseModel):
    username: str
    password: str

class DepartmentCreate(BaseModel):
    department_name: str

class EmployeeCreate(BaseModel):
    employee_name: str
    email: str
    department_id: int

class AssetCreate(BaseModel):
    asset_name: str
    asset_type: str
    serial_number: str
    purchase_cost: float

class AssetUpdate(BaseModel):
    asset_name: Optional[str] = None
    asset_type: Optional[str] = None
    purchase_cost: Optional[float] = None
    status: Optional[str] = None

class AllocationCreate(BaseModel):
    asset_id: int
    employee_id: int
    assigned_date: date

class MaintenanceCreate(BaseModel):
    asset_id: int
    issue_description: str

class MaintenanceUpdate(BaseModel):
    maintenance_status: str
    cost: float
