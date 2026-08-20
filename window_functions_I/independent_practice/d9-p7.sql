WITH salary_rank AS ( 
    SELECT
        emp_id,
        dept_id,
        name,
        salary,
        DENSE_RANK() OVER(PARTITION BY dept_id ORDER BY salary DESC) as rnk
    FROM employees
)

SELECT 
    emp_id,
    dept_id,
    name,
    salary
FROM salary_rank
WHERE rnk <= 2
ORDER BY
    dept_id ASC,
    salary DESC;