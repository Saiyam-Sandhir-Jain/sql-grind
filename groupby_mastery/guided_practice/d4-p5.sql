SELECT 
    customer_id, 
    COUNT(*) FILTER (WHERE status = 'DELIVERED') AS delivered_orders
FROM orders
GROUP BY customer_id
ORDER BY customer_id;