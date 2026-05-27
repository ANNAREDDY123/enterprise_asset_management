INSERT INTO departments (department_id, department_name) VALUES
(1, 'IT'),
(2, 'HR'),
(3, 'Finance');

INSERT INTO employees (employee_id, employee_name, email, department_id) VALUES
(1, 'Rahul', 'rahul@example.com', 1),
(2, 'Priya', 'priya@example.com', 1),
(3, 'Amit', 'amit@example.com', 2);

INSERT INTO assets (asset_id, asset_name, asset_type, serial_number, purchase_cost, status, is_deleted) VALUES
(1, 'Dell Laptop', 'Laptop', 'DL12345', 55000, 'Assigned', 0),
(2, 'HP Printer', 'Printer', 'HP98765', 18000, 'Available', 0),
(3, 'Office Chair', 'Furniture', 'CH45678', 7000, 'Maintenance', 0),
(4, 'Projector', 'Electronics', 'PJ11223', 45000, 'Available', 0);

INSERT INTO asset_allocations (allocation_id, asset_id, employee_id, assigned_date, return_date, status) VALUES
(1, 1, 1, '2026-05-01', NULL, 'Assigned'),
(2, 4, 2, '2026-01-10', '2026-03-10', 'Returned');

INSERT INTO maintenance_requests (request_id, asset_id, issue_description, maintenance_status, cost, request_date) VALUES
(1, 3, 'Chair wheel damaged', 'Pending', 0, '2026-05-15 10:00:00'),
(2, 1, 'Laptop battery replacement', 'Completed', 2500, '2026-04-20 11:30:00');

INSERT INTO audit_logs (audit_id, action, table_name, record_id, performed_by, action_time) VALUES
(1, 'ADD_ASSET', 'assets', 1, 'admin', '2026-05-15 09:00:00'),
(2, 'ASSIGN_ASSET', 'asset_allocations', 1, 'admin', '2026-05-15 09:30:00');
