SELECT 
    status,
    COUNT(*) as orders,
    MIN(order_date) as earliest_order_date
FROM orders
WHERE status IS NOT NULL
GROUP BY status;