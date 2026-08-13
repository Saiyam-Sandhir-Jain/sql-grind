SELECT dept_id, SUM(salary) as total_salary_bill
FROM employees
WHERE dept_id IS NOT NULL
GROUP BY dept_id
ORDER BY total_salary_bill;