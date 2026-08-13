SELECT dept_id, COUNT(*) AS "number of employees"
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY dept_id;