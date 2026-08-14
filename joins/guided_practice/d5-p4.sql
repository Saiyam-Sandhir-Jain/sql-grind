-- INSERT INTO departments
-- (dept_name,  location,   budget) VALUES
-- ('Legal',    'New York', 500000.00);

-- With RIGHT JOIN
SELECT d.dept_name, e.name
FROM employees AS e
RIGHT JOIN departments d ON e.dept_id = d.dept_id;

-- With LEFT JOIN
SELECT d.dept_name, e.name
FROM departments AS d
LEFT JOIN employees e ON e.dept_id = d.dept_id; 