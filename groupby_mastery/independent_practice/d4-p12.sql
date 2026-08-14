SELECT
    EXTRACT(YEAR FROM order_date) AS order_year,
    COUNT(*) as num_of_orders,
    COUNT(*) FILTER (WHERE status = 'CANCELLED')
FROM orders
GROUP BY 1
ORDER BY order_year;