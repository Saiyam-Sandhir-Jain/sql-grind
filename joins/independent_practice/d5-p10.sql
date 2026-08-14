SELECT 
    e.emp_id AS employee_id,
    e.name AS employee_name,
    m.emp_id AS manager_id,
    m.name AS manager_name,
    d.dept_name AS department
FROM employees AS e
LEFT JOIN employees AS m 
    ON e.manager_id = m.emp_id
LEFT JOIN departments AS d 
    ON e.dept_id = d.dept_id;