SELECT
    city,
    COUNT(*) as num_of_customers
FROM customers
GROUP BY city
HAVING COUNT(*) > 1;