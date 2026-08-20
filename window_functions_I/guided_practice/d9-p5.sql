SELECT
    emp_id,
    dept_id,
    ROUND(ABS(salary - AVG(salary) OVER(PARTITION BY dept_id)), 2) AS salary_diff_with_avg
FROM employees;