SELECT customer_id, COUNT(*)
FROM orders
GROUP BY customer_id
ORDER BY customer_id;