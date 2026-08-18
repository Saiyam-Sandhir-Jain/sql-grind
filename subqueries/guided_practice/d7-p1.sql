SELECT emp_id, name
FROM employees
WHERE salary > (
    SELECT AVG(salary)
    FROM employees
);