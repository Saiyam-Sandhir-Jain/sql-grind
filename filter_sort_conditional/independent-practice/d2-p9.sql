SELECT
    product_id,
    product_name,
    CASE 
        WHEN unit_price > 50000 THEN 'Premium'
        WHEN unit_price BETWEEN 5000 AND 50000 THEN 'Standard'
        ELSE 'Budget'
    END AS price_range
FROM products
ORDER BY unit_price DESC;