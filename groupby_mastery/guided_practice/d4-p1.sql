SELECT dept_id, job_title, COUNT(*)
FROM employees
GROUP BY dept_id, job_title
ORDER BY 
    dept_id ASC,
    job_title DESC;