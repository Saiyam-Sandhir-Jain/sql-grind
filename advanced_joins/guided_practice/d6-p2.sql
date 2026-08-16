SELECT
    o.order_id,
    c.customer_name,
    p.product_name
FROM orders AS o
LEFT JOIN customers c ON (o.customer_id = c.customer_id)
JOIN order_items oi ON (o.order_id = oi.order_id)
JOIN products p ON (oi.product_id = p.product_id)
ORDER BY
    o.order_id,
    p.product_name;