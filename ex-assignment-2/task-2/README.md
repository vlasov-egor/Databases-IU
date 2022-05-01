# Indexes
```
CREATE INDEX product_type_idx ON product USING hash (type);
CREATE INDEX sale_type_idx ON sale USING btree (type);
```

# 1 query 
``` 
EXPLAIN ANALYZE
SELECT *
FROM purchases_products_list
         JOIN product ON product.id = purchases_products_list.product_id
         JOIN sale ON product.type = sale.type;
```

# Without indexes
```
+------------------------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                                                |
+------------------------------------------------------------------------------------------------------------------------------------------+
|Hash Join  (cost=138.53..253.12 rows=1953 width=203) (actual time=5.378..7.536 rows=1951 loops=1)                                         |
|  Hash Cond: ((product.type)::text = (sale.type)::text)                                                                                   |
|  ->  Merge Join  (cost=137.41..225.16 rows=1951 width=189) (actual time=1.206..2.695 rows=1951 loops=1)                                  |
|        Merge Cond: (product.id = purchases_products_list.product_id)                                                                     |
|        ->  Index Scan using product_pkey on product  (cost=0.28..269.20 rows=4804 width=177) (actual time=0.010..0.396 rows=1001 loops=1)|
|        ->  Sort  (cost=137.13..142.01 rows=1951 width=12) (actual time=1.183..1.461 rows=1951 loops=1)                                   |
|              Sort Key: purchases_products_list.product_id                                                                                |
|              Sort Method: quicksort  Memory: 140kB                                                                                       |
|              ->  Seq Scan on purchases_products_list  (cost=0.00..30.51 rows=1951 width=12) (actual time=0.005..0.196 rows=1951 loops=1) |
|  ->  Hash  (cost=1.05..1.05 rows=5 width=14) (actual time=0.020..0.020 rows=5 loops=1)                                                   |
|        Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                      |
|        ->  Seq Scan on sale  (cost=0.00..1.05 rows=5 width=14) (actual time=0.015..0.016 rows=5 loops=1)                                 |
|Planning Time: 0.225 ms                                                                                                                   |
|Execution Time: 7.716 ms                                                                                                                  |
+------------------------------------------------------------------------------------------------------------------------------------------+
```

# With indexes
```
+------------------------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                                                |
+------------------------------------------------------------------------------------------------------------------------------------------+
|Merge Join  (cost=137.56..250.51 rows=1953 width=203) (actual time=1.745..3.545 rows=1951 loops=1)                                        |
|  Merge Cond: (product.id = purchases_products_list.product_id)                                                                           |
|  ->  Nested Loop  (cost=0.42..390.21 rows=4808 width=191) (actual time=0.590..1.569 rows=1001 loops=1)                                   |
|        ->  Index Scan using product_pkey on product  (cost=0.28..269.20 rows=4804 width=177) (actual time=0.006..0.236 rows=1001 loops=1)|
|        ->  Memoize  (cost=0.14..0.16 rows=1 width=14) (actual time=0.001..0.001 rows=1 loops=1001)                                       |
|              Cache Key: product.type                                                                                                     |
|              Cache Mode: logical                                                                                                         |
|              Hits: 996  Misses: 5  Evictions: 0  Overflows: 0  Memory Usage: 1kB                                                         |
|              ->  Index Scan using sale_type_idx on sale  (cost=0.13..0.15 rows=1 width=14) (actual time=0.116..0.117 rows=1 loops=5)     |
|                    Index Cond: ((type)::text = (product.type)::text)                                                                     |
|  ->  Sort  (cost=137.13..142.01 rows=1951 width=12) (actual time=1.150..1.370 rows=1951 loops=1)                                         |
|        Sort Key: purchases_products_list.product_id                                                                                      |
|        Sort Method: quicksort  Memory: 140kB                                                                                             |
|        ->  Seq Scan on purchases_products_list  (cost=0.00..30.51 rows=1951 width=12) (actual time=0.024..0.195 rows=1951 loops=1)       |
|Planning Time: 1.247 ms                                                                                                                   |
|Execution Time: 3.699 ms                                                                                                                  |
+------------------------------------------------------------------------------------------------------------------------------------------+
```

# 2 query 
``` 
EXPLAIN ANALYZE
SELECT customer.id, customer.name, customer.address, customer.product_review, SUM(discount)
FROM customer
         JOIN purchase ON purchase.customer_id = customer.id
         JOIN purchases_products_list ON purchases_products_list.purchase_id = purchase.id
         JOIN product ON purchases_products_list.product_id = product.id
         JOIN sale ON product.type = sale.type
GROUP BY customer.id;
```

# Without indexes
```
+----------------------------------------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                                                                |
+----------------------------------------------------------------------------------------------------------------------------------------------------------+
|HashAggregate  (cost=7316.94..7336.47 rows=1953 width=220) (actual time=10.132..10.418 rows=851 loops=1)                                                  |
|  Group Key: customer.id                                                                                                                                  |
|  Batches: 1  Memory Usage: 625kB                                                                                                                         |
|  ->  Hash Join  (cost=333.60..7307.18 rows=1953 width=220) (actual time=2.167..8.200 rows=1951 loops=1)                                                  |
|        Hash Cond: ((product.type)::text = (sale.type)::text)                                                                                             |
|        ->  Merge Join  (cost=332.48..7279.22 rows=1951 width=214) (actual time=2.140..7.555 rows=1951 loops=1)                                           |
|              Merge Cond: (purchase.id = purchases_products_list.purchase_id)                                                                             |
|              ->  Nested Loop  (cost=0.71..20067.95 rows=2902 width=216) (actual time=0.016..4.489 rows=1001 loops=1)                                     |
|                    ->  Index Scan using purchase_pkey on purchase  (cost=0.28..99.81 rows=2902 width=8) (actual time=0.007..0.242 rows=1001 loops=1)     |
|                    ->  Index Scan using customer_pkey on customer  (cost=0.42..6.88 rows=1 width=212) (actual time=0.004..0.004 rows=1 loops=1001)       |
|                          Index Cond: (id = purchase.customer_id)                                                                                         |
|              ->  Sort  (cost=331.78..336.66 rows=1951 width=6) (actual time=2.121..2.427 rows=1951 loops=1)                                              |
|                    Sort Key: purchases_products_list.purchase_id                                                                                         |
|                    Sort Method: quicksort  Memory: 140kB                                                                                                 |
|                    ->  Merge Join  (cost=137.41..225.16 rows=1951 width=6) (actual time=0.732..1.633 rows=1951 loops=1)                                  |
|                          Merge Cond: (product.id = purchases_products_list.product_id)                                                                   |
|                          ->  Index Scan using product_pkey on product  (cost=0.28..269.20 rows=4804 width=6) (actual time=0.005..0.218 rows=1001 loops=1)|
|                          ->  Sort  (cost=137.13..142.01 rows=1951 width=8) (actual time=0.723..0.890 rows=1951 loops=1)                                  |
|                                Sort Key: purchases_products_list.product_id                                                                              |
|                                Sort Method: quicksort  Memory: 140kB                                                                                     |
|                                ->  Seq Scan on purchases_products_list  (cost=0.00..30.51 rows=1951 width=8) (actual time=0.005..0.289 rows=1951 loops=1)|
|        ->  Hash  (cost=1.05..1.05 rows=5 width=10) (actual time=0.014..0.016 rows=5 loops=1)                                                             |
|              Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                                |
|              ->  Seq Scan on sale  (cost=0.00..1.05 rows=5 width=10) (actual time=0.010..0.011 rows=5 loops=1)                                           |
|Planning Time: 0.683 ms                                                                                                                                   |
|Execution Time: 11.189 ms                                                                                                                                 |
+----------------------------------------------------------------------------------------------------------------------------------------------------------+
```

# With indexes
```
+----------------------------------------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                                                                |
+----------------------------------------------------------------------------------------------------------------------------------------------------------+
|HashAggregate  (cost=7316.94..7336.47 rows=1953 width=220) (actual time=10.191..10.385 rows=851 loops=1)                                                  |
|  Group Key: customer.id                                                                                                                                  |
|  Batches: 1  Memory Usage: 625kB                                                                                                                         |
|  ->  Hash Join  (cost=333.60..7307.18 rows=1953 width=220) (actual time=3.088..9.291 rows=1951 loops=1)                                                  |
|        Hash Cond: ((product.type)::text = (sale.type)::text)                                                                                             |
|        ->  Merge Join  (cost=332.48..7279.22 rows=1951 width=214) (actual time=1.974..7.568 rows=1951 loops=1)                                           |
|              Merge Cond: (purchase.id = purchases_products_list.purchase_id)                                                                             |
|              ->  Nested Loop  (cost=0.71..20067.95 rows=2902 width=216) (actual time=0.018..4.606 rows=1001 loops=1)                                     |
|                    ->  Index Scan using purchase_pkey on purchase  (cost=0.28..99.81 rows=2902 width=8) (actual time=0.008..0.249 rows=1001 loops=1)     |
|                    ->  Index Scan using customer_pkey on customer  (cost=0.42..6.88 rows=1 width=212) (actual time=0.004..0.004 rows=1 loops=1001)       |
|                          Index Cond: (id = purchase.customer_id)                                                                                         |
|              ->  Sort  (cost=331.78..336.66 rows=1951 width=6) (actual time=1.953..2.293 rows=1951 loops=1)                                              |
|                    Sort Key: purchases_products_list.purchase_id                                                                                         |
|                    Sort Method: quicksort  Memory: 140kB                                                                                                 |
|                    ->  Merge Join  (cost=137.41..225.16 rows=1951 width=6) (actual time=0.626..1.550 rows=1951 loops=1)                                  |
|                          Merge Cond: (product.id = purchases_products_list.product_id)                                                                   |
|                          ->  Index Scan using product_pkey on product  (cost=0.28..269.20 rows=4804 width=6) (actual time=0.006..0.220 rows=1001 loops=1)|
|                          ->  Sort  (cost=137.13..142.01 rows=1951 width=8) (actual time=0.616..0.793 rows=1951 loops=1)                                  |
|                                Sort Key: purchases_products_list.product_id                                                                              |
|                                Sort Method: quicksort  Memory: 140kB                                                                                     |
|                                ->  Seq Scan on purchases_products_list  (cost=0.00..30.51 rows=1951 width=8) (actual time=0.005..0.228 rows=1951 loops=1)|
|        ->  Hash  (cost=1.05..1.05 rows=5 width=10) (actual time=0.021..0.022 rows=5 loops=1)                                                             |
|              Buckets: 1024  Batches: 1  Memory Usage: 9kB                                                                                                |
|              ->  Seq Scan on sale  (cost=0.00..1.05 rows=5 width=10) (actual time=0.014..0.015 rows=5 loops=1)                                           |
|Planning Time: 0.538 ms                                                                                                                                   |
|Execution Time: 10.582 ms                                                                                                                                 |
+----------------------------------------------------------------------------------------------------------------------------------------------------------+
```










