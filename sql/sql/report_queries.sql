-- 1. Find most assigned assets
SELECT a.asset_name, COUNT(aa.allocation_id) AS assigned_count
FROM assets a
JOIN asset_allocations aa ON a.asset_id = aa.asset_id
GROUP BY a.asset_id, a.asset_name
ORDER BY assigned_count DESC;

-- 2. Employees holding multiple assets
SELECT e.employee_name, COUNT(aa.asset_id) AS total_assets
FROM employees e
JOIN asset_allocations aa ON e.employee_id = aa.employee_id
WHERE aa.status = 'Assigned'
GROUP BY e.employee_id, e.employee_name
HAVING COUNT(aa.asset_id) > 1;

-- 3. Monthly maintenance cost report
SELECT strftime('%Y-%m', request_date) AS month,
       SUM(cost) AS total_maintenance_cost
FROM maintenance_requests
GROUP BY strftime('%Y-%m', request_date)
ORDER BY month;

-- 4. Assets not used for last 6 months
SELECT a.asset_name
FROM assets a
LEFT JOIN asset_allocations aa ON a.asset_id = aa.asset_id
GROUP BY a.asset_id, a.asset_name
HAVING MAX(aa.assigned_date) < date('now', '-6 months')
   OR MAX(aa.assigned_date) IS NULL;

-- 5. Asset utilization percentage
SELECT
    ROUND(
        SUM(CASE WHEN status = 'Assigned' THEN 1 ELSE 0 END) * 100.0 / COUNT(*),
        2
    ) AS utilization_percentage
FROM assets
WHERE is_deleted = FALSE;

-- 6. Department-wise asset allocation report
SELECT d.department_name, COUNT(aa.asset_id) AS total_allocated_assets
FROM departments d
JOIN employees e ON d.department_id = e.department_id
JOIN asset_allocations aa ON e.employee_id = aa.employee_id
WHERE aa.status = 'Assigned'
GROUP BY d.department_id, d.department_name;

-- 7. Top 5 expensive assets
SELECT asset_name, asset_type, purchase_cost
FROM assets
WHERE is_deleted = FALSE
ORDER BY purchase_cost DESC
LIMIT 5;

-- 8. Assets under maintenance with pending requests
SELECT a.asset_name, mr.issue_description, mr.maintenance_status
FROM assets a
JOIN maintenance_requests mr ON a.asset_id = mr.asset_id
WHERE a.status = 'Maintenance'
AND mr.maintenance_status = 'Pending';

-- 9. Employee asset audit report using JOINs
SELECT e.employee_name,
       d.department_name,
       a.asset_name,
       aa.assigned_date,
       aa.return_date,
       aa.status
FROM asset_allocations aa
JOIN employees e ON aa.employee_id = e.employee_id
JOIN departments d ON e.department_id = d.department_id
JOIN assets a ON aa.asset_id = a.asset_id
ORDER BY e.employee_name, aa.assigned_date;

-- 10. Rank departments by asset value using Window Functions
SELECT department_name,
       total_asset_value,
       RANK() OVER(ORDER BY total_asset_value DESC) AS department_rank
FROM (
    SELECT d.department_name,
           SUM(a.purchase_cost) AS total_asset_value
    FROM departments d
    JOIN employees e ON d.department_id = e.department_id
    JOIN asset_allocations aa ON e.employee_id = aa.employee_id
    JOIN assets a ON aa.asset_id = a.asset_id
    WHERE aa.status = 'Assigned'
    GROUP BY d.department_id, d.department_name
) AS department_values;
