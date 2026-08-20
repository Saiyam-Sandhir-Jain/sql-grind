WITH RankedSalaries AS (
    SELECT
        emp_id,
        dept_id,
        salary,
        ROW_NUMBER() OVER(PARTITION BY dept_id ORDER BY salary DESC) as rn
    FROM employees
)

SELECT
    emp_id,
    dept_id,
    salary
FROM RankedSalaries
WHERE rn = 1;