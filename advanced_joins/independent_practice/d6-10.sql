WITH
    project_leads AS (
        SELECT
            ep.project_id,
            e.name AS lead_name,
            e.emp_id
        FROM employee_projects ep
        JOIN employees e ON ep.emp_id = e.emp_id
        WHERE role = 'Lead'
    ),

    project_total_hours AS (
        SELECT
            project_id,
            SUM(hours_worked) AS total_hours
        FROM employee_projects
        GROUP BY project_id
    )

SELECT
    p.project_id,
    pl.emp_id AS lead_emp_id,
    COALESCE(pl.lead_name, 'No Lead Assigned') AS lead_name,
    COALESCE(pth.total_hours, 0) AS total_hours_worked
FROM projects AS p
LEFT JOIN project_leads pl ON (p.project_id = pl.project_id)
LEFT JOIN project_total_hours pth ON (p.project_id = pth.project_id)
ORDER BY p.project_id;
