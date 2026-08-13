SELECT category, AVG(unit_price) AS avg_price
FROM products
GROUP BY category;