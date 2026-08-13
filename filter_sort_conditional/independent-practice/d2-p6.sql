SELECT emp_id, name, dept_id, salary
FROM employees
ORDER BY
    dept_id ASC NULLS FIRST,
    salary DESC;