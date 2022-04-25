create INDEX payment_idx on payment using btree (payment_id, customer_id, staff_id, rental_id, payment_date);
create INDEX rental_idx on rental using btree (last_update);

create INDEX film_idx on film using btree (release_year, rental_rate);


CREATE INDEX inventory_idx ON inventory USING btree (film_id, inventory_id);
CREATE INDEX film_idx1 ON film USING hash (film_id);
CREATE INDEX film_actor_idx ON film_actor USING btree (film_id, actor_id);
CREATE INDEX rental_idx1 ON rental USING btree (inventory_id,customer_id);
CREATE INDEX customer_id1 ON customer USING hash (first_name);
CREATE INDEX actor_idx ON actor USING hash (first_name);
CREATE INDEX customer_idx ON customer USING hash (customer_id);
CREATE INDEX payment_idx2 ON payment USING hash (amount);
CREATE INDEX payment_idx1 ON payment USING hash (rental_id);
CREATE INDEX rental_idx2 ON rental USING hash (inventory_id);

