SELECT
    d.dept_id,
    d.dept_name,
    COUNT(DISTINCT e.manager_id) AS manager_count,
    COUNT(e.emp_id) AS total_headcount
FROM departments d
LEFT JOIN employees e ON d.dept_id = e.dept_id
GROUP BY d.dept_id, d.dept_name;