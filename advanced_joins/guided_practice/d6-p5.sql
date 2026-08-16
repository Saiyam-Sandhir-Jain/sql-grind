SELECT
    e.emp_id,
    e.name
FROM employees AS e
WHERE NOT EXISTS (
    SELECT 1 
    FROM employee_projects AS ep 
    WHERE e.emp_id = ep.emp_id
)
ORDER BY e.emp_id;