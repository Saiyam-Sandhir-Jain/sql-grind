WITH projects_total AS (
    SELECT 
        dept_id, 
        COUNT(*) AS total_projects 
    FROM projects 
    GROUP BY dept_id
),
employees_total AS (
    SELECT 
        dept_id, 
        COUNT(*) AS total_employees 
    FROM employees 
    GROUP BY dept_id
)
SELECT 
    d.dept_id, 
    COALESCE(pt.total_projects, 0) AS total_projects,
    COALESCE(et.total_employees, 0) AS total_employees
FROM departments d
LEFT JOIN projects_total pt ON d.dept_id = pt.dept_id
LEFT JOIN employees_total et ON d.dept_id = et.dept_id;