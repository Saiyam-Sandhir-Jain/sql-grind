SELECT e.name, d.dept_name
FROM employees AS e
LEFT JOIN departments d ON e.dept_id = d.dept_id;