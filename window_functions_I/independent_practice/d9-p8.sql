WITH salary_ranks AS (
    SELECT
        salary,
        DENSE_RANK() OVER(ORDER BY salary DESC) as ranks
    FROM
        employees
)

SELECT DISTINCT
    salary
FROM salary_ranks
WHERE ranks = 3;