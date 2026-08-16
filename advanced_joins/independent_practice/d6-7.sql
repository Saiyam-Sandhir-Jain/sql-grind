SELECT
    p.product_id
FROM products AS p 
WHERE NOT EXISTS (
    SELECT 1
    FROM order_items AS oi
    WHERE p.product_id = oi.product_id
);