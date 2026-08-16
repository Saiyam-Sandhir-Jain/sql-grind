SELECT 
    e.name AS employee_name,
    p.project_name,
    ep.hours_worked
FROM employees AS e
JOIN employee_projects ep ON (e.emp_id = ep.emp_id)
JOIN projects p ON (ep.project_id = p.project_id)
ORDER BY 
    employee_name,
    hours_worked DESC,
    project_name;