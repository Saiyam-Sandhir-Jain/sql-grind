SELECT
    dept_id,
    COUNT(*) FILTER (WHERE hire_date < '01-01-2020') AS hired_before_2020,
    COUNT(*) FILTER (WHERE hire_date >= '01-01-2020') AS hired_in_or_after_2020
FROM employees
GROUP BY dept_id
ORDER BY dept_id;