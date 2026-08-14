SELECT
    job_title,
    COUNT(*) AS num_of_employees,
    MIN(salary) || '-' || MAX(salary) as salary_range
FROM employees
GROUP BY job_title
ORDER BY num_of_employees;