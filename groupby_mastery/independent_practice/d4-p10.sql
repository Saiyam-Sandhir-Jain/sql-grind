SELECT
    dept_id,
    COUNT(*) FILTER (WHERE salary > 90000) as high_earners,
    ROUND(COUNT(*) FILTER (WHERE salary > 90000) * 100.0 / COUNT(*), 1) AS high_earners_percentage
FROM employees
GROUP BY dept_id
ORDER BY dept_id;