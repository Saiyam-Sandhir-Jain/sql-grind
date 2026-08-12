SELECT emp_id, name
FROM employees
WHERE dept_id != 1 OR dept_id IS NULL;