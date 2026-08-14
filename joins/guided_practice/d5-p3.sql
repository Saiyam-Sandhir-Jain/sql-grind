SELECT o.order_id, c.customer_name
FROM orders as o
JOIN customers c ON o.customer_id = c.customer_id;