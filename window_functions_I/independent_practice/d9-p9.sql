WITH order_ranks AS (
    SELECT
        o.customer_id,
        o.order_id,
        SUM(oi.quantity * oi.unit_price) AS total_price,
        DENSE_RANK() OVER(PARTITION BY o.customer_id ORDER BY SUM(oi.quantity * oi.unit_price) DESC) AS order_rank
    FROM orders AS o
    JOIN order_items oi ON (o.order_id = oi.order_id)
    GROUP BY 
        o.customer_id,
        o.order_id
)

SELECT
    customer_id,
    order_id,
    total_price
FROM order_ranks
WHERE order_rank = 1;