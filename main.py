from fastapi import FastAPI, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from datetime import date

from database import Base, engine, get_db
import models
import schemas
from auth import hash_password, verify_password, create_access_token, get_current_user, admin_required

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Enterprise Asset Management System")

@app.get("/")
def home():
    return {"message": "Enterprise Asset Management API is running"}

@app.post("/register")
def register(user: schemas.UserRegister, db: Session = Depends(get_db)):
    existing_user = db.query(models.User).filter(models.User.username == user.username).first()

    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")

    new_user = models.User(
        username=user.username,
        password=hash_password(user.password),
        role=user.role)

    db.add(new_user)
    db.commit()

    return {"message": "User registered successfully"}

@app.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.username == user.username).first()

    if not db_user or not verify_password(user.password, db_user.password):
        raise HTTPException(status_code=401, detail="Invalid username or password")

    token = create_access_token({"sub": db_user.username, "role": db_user.role})

    return {"access_token": token, "token_type": "bearer"}

@app.post("/departments")
def add_department(
    department: schemas.DepartmentCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    new_department = models.Department(department_name=department.department_name)
    db.add(new_department)
    db.commit()

    return {"message": "Department added successfully"}

@app.post("/employees")
def add_employee(
    employee: schemas.EmployeeCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    new_employee = models.Employee(**employee.dict())
    db.add(new_employee)
    db.commit()

    return {"message": "Employee added successfully"}

@app.post("/assets")
def add_asset(
    asset: schemas.AssetCreate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    new_asset = models.Asset(**asset.dict())

    db.add(new_asset)
    db.commit()
    db.refresh(new_asset)

    audit = models.AuditLog(
        action="ADD_ASSET",
        table_name="assets",
        record_id=new_asset.asset_id,
        performed_by=current_user.get("sub")
    )

    db.add(audit)
    db.commit()

    return {"message": "Asset added successfully", "asset_id": new_asset.asset_id}

@app.get("/assets")
def view_assets(
    search: str = "",
    status: str = "",
    page: int = Query(1, ge=1),
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    query = db.query(models.Asset).filter(models.Asset.is_deleted == False)

    if search:
        query = query.filter(models.Asset.asset_name.like(f"%{search}%"))

    if status:
        query = query.filter(models.Asset.status == status)

    total = query.count()
    assets = query.offset((page - 1) * limit).limit(limit).all()

    return {
        "total": total,
        "page": page,
        "limit": limit,
        "assets": assets
    }

@app.put("/assets/{asset_id}")
def update_asset(
    asset_id: int,
    asset: schemas.AssetUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    db_asset = db.query(models.Asset).filter(
        models.Asset.asset_id == asset_id,
        models.Asset.is_deleted == False
    ).first()

    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    for key, value in asset.dict(exclude_unset=True).items():
        setattr(db_asset, key, value)

    db.commit()

    return {"message": "Asset updated successfully"}

@app.delete("/assets/{asset_id}")
def soft_delete_asset(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    db_asset = db.query(models.Asset).filter(models.Asset.asset_id == asset_id).first()

    if not db_asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    db_asset.is_deleted = True
    db_asset.status = "Retired"

    db.commit()

    return {"message": "Asset soft deleted successfully"}

@app.post("/allocate")
def assign_asset(
    allocation: schemas.AllocationCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    asset = db.query(models.Asset).filter(
        models.Asset.asset_id == allocation.asset_id,
        models.Asset.is_deleted == False
    ).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset.status == "Assigned":
        raise HTTPException(status_code=400, detail="Asset is already assigned")

    new_allocation = models.AssetAllocation(**allocation.dict())
    asset.status = "Assigned"

    db.add(new_allocation)
    db.commit()

    return {"message": "Asset assigned successfully"}

@app.put("/return/{allocation_id}")
def return_asset(
    allocation_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    allocation = db.query(models.AssetAllocation).filter(
        models.AssetAllocation.allocation_id == allocation_id
    ).first()

    if not allocation:
        raise HTTPException(status_code=404, detail="Allocation not found")

    allocation.return_date = date.today()
    allocation.status = "Returned"

    asset = db.query(models.Asset).filter(models.Asset.asset_id == allocation.asset_id).first()
    asset.status = "Available"

    db.commit()

    return {"message": "Asset returned successfully"}

@app.get("/asset-history/{asset_id}")
def asset_history(
    asset_id: int,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    history = db.query(models.AssetAllocation).filter(
        models.AssetAllocation.asset_id == asset_id
    ).all()

    return history

@app.post("/maintenance")
def raise_maintenance(
    request: schemas.MaintenanceCreate,
    db: Session = Depends(get_db),
    current_user=Depends(get_current_user)
):
    asset = db.query(models.Asset).filter(models.Asset.asset_id == request.asset_id).first()

    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    asset.status = "Maintenance"

    maintenance = models.MaintenanceRequest(**request.dict())
    db.add(maintenance)
    db.commit()

    return {"message": "Maintenance request raised"}

@app.put("/maintenance/{request_id}")
def update_maintenance(
    request_id: int,
    update: schemas.MaintenanceUpdate,
    db: Session = Depends(get_db),
    current_user=Depends(admin_required)
):
    maintenance = db.query(models.MaintenanceRequest).filter(
        models.MaintenanceRequest.request_id == request_id
    ).first()

    if not maintenance:
        raise HTTPException(status_code=404, detail="Maintenance request not found")

    maintenance.maintenance_status = update.maintenance_status
    maintenance.cost = update.cost

    if update.maintenance_status == "Completed":
        asset = db.query(models.Asset).filter(models.Asset.asset_id == maintenance.asset_id).first()
        asset.status = "Available"

    db.commit()

    return {"message": "Maintenance updated successfully"}
