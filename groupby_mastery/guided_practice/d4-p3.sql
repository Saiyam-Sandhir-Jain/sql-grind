SELECT 
    EXTRACT(YEAR FROM hire_date) AS hire_year,
    COUNT(*)
FROM employees
GROUP BY 1
ORDER BY hire_year;