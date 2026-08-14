SELECT o.order_id, c.customer_name, c.country
FROM orders AS o
LEFT JOIN customers c ON o.customer_id = c.customer_id 
WHERE o.status = 'DELIVERED';