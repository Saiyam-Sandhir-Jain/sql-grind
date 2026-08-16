WITH
    revenue_from_customers AS (
        SELECT
            o.customer_id,
            SUM(quantity * unit_price) AS revenue
        FROM orders AS o
        JOIN order_items oi ON (o.order_id = oi.order_id)
        GROUP BY o.customer_id
    )

SELECT
    c.customer_id,
    c.customer_name,
    c.country,
    COALESCE(rfc.revenue, 0) AS revenue
FROM customers AS c
LEFT JOIN revenue_from_customers rfc ON (c.customer_id = rfc.customer_id)
ORDER BY revenue DESC
LIMIT 3;