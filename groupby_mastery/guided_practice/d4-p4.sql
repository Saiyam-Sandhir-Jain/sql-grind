SELECT 
    category,
    COUNT(*), 
    MIN(unit_price) AS min_price, 
    MAX(unit_price) AS max_price
FROM products
GROUP BY category
ORDER BY
    COUNT(*) ASC,
    min_price DESC,
    max_price ASC;