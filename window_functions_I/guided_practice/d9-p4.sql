SELECT
    emp_id,
    dept_id,
    name,
    salary,
    DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC)
FROM employees
ORDER BY 
    dept_id ASC,
    salary DESC,
    emp_id ASC;