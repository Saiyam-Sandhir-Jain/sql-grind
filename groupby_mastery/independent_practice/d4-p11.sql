SELECT
    project_id,
    COUNT(*) AS num_of_employees,
    SUM(hours_worked) AS total_hours_worked
FROM employee_projects
GROUP BY project_id
ORDER BY project_id;