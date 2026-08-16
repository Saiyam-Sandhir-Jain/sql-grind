SELECT dept_id, COUNT(*) AS number_of_projects
FROM projects
GROUP BY dept_id
ORDER BY dept_id;