SELECT 
    e.name AS emp_name,
    m.name AS manager_name
FROM employees e 
LEFT JOIN employees m on e.manager_id = m.emp_id;