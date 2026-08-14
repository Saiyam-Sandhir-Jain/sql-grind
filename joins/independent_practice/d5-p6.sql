SELECT e.name
FROM employees AS e
JOIN departments d ON e.dept_id = d.dept_id
WHERE 
    e.salary > 80000
    AND d.location = 'Bangalore';