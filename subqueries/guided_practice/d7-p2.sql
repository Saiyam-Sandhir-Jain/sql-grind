SELECT 
    emp_id, 
    name, 
    dept_id
FROM employees
WHERE dept_id IN (
    SELECT dept_id
    FROM departments
    WHERE location = 'Bangalore'
);