SELECT
    emp_id,
    dept_id,
    name,
    AVG(salary) OVER(PARTITION BY dept_id) AS dept_avg_salary
FROM employees;