SELECT emp_id, name
FROM employees
WHERE (salary > 90000 OR hire_date < '01-01-2016') AND dept_id != 4;