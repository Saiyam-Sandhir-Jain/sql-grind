SELECT 
    emp_id,
    name,
    CASE
        WHEN manager_id IS NULL THEN 'No'
        ELSE 'YES'
    END AS has_manager
FROM employees
ORDER BY
    manager_id NULLS FIRST,
    salary DESC;