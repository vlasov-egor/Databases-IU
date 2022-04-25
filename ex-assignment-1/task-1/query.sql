SELECT DISTINCT customer."customer_id",
                customer."store_id",
                customer."first_name",
                customer."last_name",
                customer."email",
                customer."address_id",
                customer."activebool",
                customer."create_date",
                customer."last_update",
                customer."active"
FROM "customer"
JOIN "rental" ON rental."customer_id" = customer."customer_id"
JOIN "inventory" ON inventory."inventory_id" = rental."inventory_id"
JOIN "film" ON film."film_id" = inventory."film_id"
WHERE "replacement_cost" = 14