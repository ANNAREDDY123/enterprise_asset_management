CREATE TABLE users (
    user_id INTEGER PRIMARY KEY AUTOINCREMENT,
    username VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    role VARCHAR(50) NOT NULL);

CREATE TABLE departments (
    department_id INTEGER PRIMARY KEY AUTOINCREMENT,
    department_name VARCHAR(100) NOT NULL);

CREATE TABLE employees (
    employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    employee_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE,
    department_id INTEGER,
    FOREIGN KEY (department_id) REFERENCES departments(department_id));

CREATE TABLE assets (
    asset_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_name VARCHAR(100) NOT NULL,
    asset_type VARCHAR(100),
    serial_number VARCHAR(100) UNIQUE,
    purchase_cost FLOAT,
    status VARCHAR(50) DEFAULT 'Available',
    is_deleted BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP);

CREATE TABLE asset_allocations (
    allocation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER,
    employee_id INTEGER,
    assigned_date DATE,
    return_date DATE,
    status VARCHAR(50) DEFAULT 'Assigned',
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id),
    FOREIGN KEY (employee_id) REFERENCES employees(employee_id));

CREATE TABLE maintenance_requests (
    request_id INTEGER PRIMARY KEY AUTOINCREMENT,
    asset_id INTEGER,
    issue_description TEXT,
    maintenance_status VARCHAR(50) DEFAULT 'Pending',
    cost FLOAT DEFAULT 0,
    request_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (asset_id) REFERENCES assets(asset_id));

CREATE TABLE audit_logs (
    audit_id INTEGER PRIMARY KEY AUTOINCREMENT,
    action VARCHAR(100),
    table_name VARCHAR(100),
    record_id INTEGER,
    performed_by VARCHAR(100),
    action_time DATETIME DEFAULT CURRENT_TIMESTAMP);
