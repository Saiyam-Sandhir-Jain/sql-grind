-- Containing customers with no orders
WITH order_totals AS (
    SELECT 
        order_id, 
        SUM(quantity * unit_price) AS order_revenue
    FROM order_items
    GROUP BY order_id
)

SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS num_of_orders,
    COALESCE(SUM(ot.order_revenue), 0) AS total_revenue
FROM customers c
LEFT JOIN orders o ON c.customer_id = o.customer_id
LEFT JOIN order_totals ot ON o.order_id = ot.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id;


-- Not contianing customers with no orders
WITH order_totals AS (
    SELECT 
        order_id, 
        SUM(quantity * unit_price) AS order_revenue
    FROM order_items
    GROUP BY order_id
)

SELECT 
    c.customer_id,
    c.customer_name,
    COUNT(o.order_id) AS num_of_orders,
    COALESCE(SUM(ot.order_revenue), 0) AS total_revenue
FROM customers c
INNER JOIN orders o ON c.customer_id = o.customer_id
INNER JOIN order_totals ot ON o.order_id = ot.order_id
GROUP BY c.customer_id, c.customer_name
ORDER BY c.customer_id;