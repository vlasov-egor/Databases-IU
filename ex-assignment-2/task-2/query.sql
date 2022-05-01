SELECT *
FROM purchases_products_list
JOIN product ON product.id = purchases_products_list.product_id
JOIN sale ON product.type = sale.type;


SELECT customer.id,
       customer.name,
       customer.address,
       customer.product_review,
       SUM(discount)
FROM customer
JOIN purchase ON purchase.customer_id = customer.id
JOIN purchases_products_list ON purchases_products_list.purchase_id = purchase.id
JOIN product ON purchases_products_list.product_id = product.id
JOIN sale ON product.type = sale.type
GROUP BY customer.id;

