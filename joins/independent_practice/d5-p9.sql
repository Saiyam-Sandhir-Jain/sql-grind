SELECT c.customer_name 
FROM customers AS c
LEFT JOIN orders o ON c.customer_id = o.customer_id 
WHERE o.customer_id IS NULL;