SELECT
    emp_id,
    name,
    AVG(salary) OVER() AS avg_salary
FROM employees;