-- Cleaned & Optimized Version
SELECT
    p.project_id,
    p.project_name,
    COUNT(ep.emp_id) AS num_of_employees
FROM projects AS p 
JOIN employee_projects ep ON p.project_id = ep.project_id
GROUP BY p.project_id, p.project_name
ORDER BY 
    p.project_id ASC,
    num_of_employees DESC;