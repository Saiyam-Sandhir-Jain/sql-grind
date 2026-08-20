SELECT
    emp_id,
    name,
    salary,
    ROW_NUMBER() OVER (ORDER BY salary DESC, emp_id ASC),
    RANK() OVER (ORDER BY salary DESC),
    DENSE_RANK() OVER (ORDER BY salary DESC)
FROM employees;