SELECT 
    category,
    COUNT(*) AS num_of_products,
    AVG(unit_price) AS avg_price
FROM products
GROUP BY category
HAVING
    COUNT(*) >= 2
    AND AVG(unit_price) > 10000;