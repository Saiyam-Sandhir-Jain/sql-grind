SELECT 
    p.product_id, 
    COALESCE(SUM(oi.quantity), 0) AS total_qty_ordered
FROM products AS p 
LEFT JOIN order_items oi ON p.product_id = oi.product_id
GROUP BY p.product_id
ORDER BY p.product_id;