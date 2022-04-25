SELECT customer."customer_id",
       customer."store_id",
       customer."first_name",
       customer."last_name",
       customer."email",
       customer."address_id",
       customer."activebool",
       customer."create_date",
       customer."last_update",
       customer."active",
       payment_join.total
FROM "customer"
JOIN
    (SELECT customer_id,
            SUM(amount) as total
     FROM "payment"
     GROUP BY "customer_id") payment_join ON payment_join.customer_id = customer.customer_id
JOIN "rental" ON rental."customer_id" = customer."customer_id"
JOIN "payment" ON payment."rental_id" = rental."rental_id"
JOIN "inventory" ON inventory."inventory_id" = rental."inventory_id"
JOIN "film" ON film."film_id" = inventory."film_id"
WHERE "replacement_cost" = 14
    OR (payment.amount > 2.99
        AND total < 5)