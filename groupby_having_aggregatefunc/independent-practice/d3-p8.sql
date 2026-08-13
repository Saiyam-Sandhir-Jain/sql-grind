SELECT dept_id, AVG(salary) as avg_salary
FROM employees
GROUP BY dept_id
HAVING AVG(salary) > 80000
ORDER BY dept_id;