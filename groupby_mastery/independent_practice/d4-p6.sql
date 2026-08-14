SELECT 
    dept_id,
    COUNT(*) as head_count,
    SUM(salary) as total_salary
FROM employees
GROUP BY dept_id
HAVING SUM(salary) > 300000
ORDER BY dept_id;