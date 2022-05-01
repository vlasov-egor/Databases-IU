# Indexes
```
CREATE INDEX customer_id_idx ON customer USING hash (id);
CREATE INDEX customer_name_idx ON customer USING btree (name);
CREATE INDEX customer_address_idx ON customer USING GIN (to_tsvector('english', address));
CREATE INDEX customer_product_review_idx ON customer USING brin (product_review);
```

# 1 query 
```
EXPLAIN ANALYZE
SELECT customer.id             AS customer_id,
       customer.name           AS customer_name,
       customer.address        AS customer_address,
       customer.product_review AS customer_product_review
FROM customer
WHERE customer.id = 1
```

## Without index
```
+------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                              |
+------------------------------------------------------------------------------------------------------------------------+
|Index Scan using customer_pkey on customer  (cost=0.42..8.44 rows=1 width=212) (actual time=0.870..0.872 rows=1 loops=1)|
|  Index Cond: (id = 1)                                                                                                  |
|Planning Time: 2.894 ms                                                                                                 |
|Execution Time: 1.030 ms                                                                                                |
+------------------------------------------------------------------------------------------------------------------------+
```

## With index

```
+--------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                                |
+--------------------------------------------------------------------------------------------------------------------------+
|Index Scan using customer_id_idx on customer  (cost=0.00..8.02 rows=1 width=212) (actual time=0.044..0.056 rows=1 loops=1)|
|  Index Cond: (id = 1)                                                                                                    |
|Planning Time: 1.481 ms                                                                                                   |
|Execution Time: 0.079 ms                                                                                                  |
+--------------------------------------------------------------------------------------------------------------------------+
```

# 2 query 

```
EXPLAIN ANALYZE
SELECT customer.id             AS customer_id,
       customer.name           AS customer_name,
       customer.address        AS customer_address,
       customer.product_review AS customer_product_review
FROM customer
WHERE (customer.name LIKE 'C%')
```

## Without index
```
+----------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                      |
+----------------------------------------------------------------------------------------------------------------+
|Seq Scan on customer  (cost=0.00..42805.39 rows=80782 width=212) (actual time=0.033..425.430 rows=78116 loops=1)|
|  Filter: ((name)::text ~~ 'C%'::text)                                                                          |
|  Rows Removed by Filter: 921835                                                                                |
|Planning Time: 0.599 ms                                                                                         |
|Execution Time: 431.841 ms                                                                                      |
+----------------------------------------------------------------------------------------------------------------+
```

## With index
```
+-------------------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                                           |
+-------------------------------------------------------------------------------------------------------------------------------------+
|Bitmap Heap Scan on customer  (cost=1492.59..32798.55 rows=80782 width=212) (actual time=18.672..241.767 rows=78116 loops=1)         |
|  Filter: ((name)::text ~~ 'C%'::text)                                                                                               |
|  Heap Blocks: exact=28254                                                                                                           |
|  ->  Bitmap Index Scan on customer_name_idx  (cost=0.00..1472.39 rows=79997 width=0) (actual time=12.268..12.268 rows=78116 loops=1)|
|        Index Cond: (((name)::text >= 'C'::text) AND ((name)::text < 'D'::text))                                                     |
|Planning Time: 0.520 ms                                                                                                              |
|Execution Time: 247.505 ms                                                                                                           |
+-------------------------------------------------------------------------------------------------------------------------------------+
```

# 3 query
```
EXPLAIN ANALYZE
SELECT customer.id             AS customer_id,
       customer.name           AS customer_name,
       customer.address        AS customer_address,
       customer.product_review AS customer_product_review
FROM customer
WHERE customer.address = '2772 Daniel Junction Zacharyberg, IL 19814'
```

## Without index
```
+-------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                               |
+-------------------------------------------------------------------------------------------------------------------------+
|Gather  (cost=1000.00..36514.18 rows=1 width=212) (actual time=352.262..357.091 rows=0 loops=1)                          |
|  Workers Planned: 2                                                                                                     |
|  Workers Launched: 2                                                                                                    |
|  ->  Parallel Seq Scan on customer  (cost=0.00..35514.08 rows=1 width=212) (actual time=343.100..343.100 rows=0 loops=3)|
|        Filter: ((address)::text = '2772 Daniel Junction Zacharyberg, IL 19814'::text)                                   |
|        Rows Removed by Filter: 333317                                                                                   |
|Planning Time: 2.856 ms                                                                                                  |
|Execution Time: 357.120 ms                                                                                               |
+-------------------------------------------------------------------------------------------------------------------------+
```

## With index
```
+-------------------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                               |
+-------------------------------------------------------------------------------------------------------------------------+
|Gather  (cost=1000.00..36514.18 rows=1 width=212) (actual time=210.662..217.388 rows=0 loops=1)                          |
|  Workers Planned: 2                                                                                                     |
|  Workers Launched: 2                                                                                                    |
|  ->  Parallel Seq Scan on customer  (cost=0.00..35514.08 rows=1 width=212) (actual time=205.264..205.265 rows=0 loops=3)|
|        Filter: ((address)::text = '2772 Daniel Junction Zacharyberg, IL 19814'::text)                                   |
|        Rows Removed by Filter: 333317                                                                                   |
|Planning Time: 1.180 ms                                                                                                  |
|Execution Time: 217.431 ms                                                                                               |
+-------------------------------------------------------------------------------------------------------------------------+
```

# 4 query
```
EXPLAIN ANALYZE
SELECT customer.id             AS customer_id,
       customer.name           AS customer_name,
       customer.address        AS customer_address,
       customer.product_review AS customer_product_review
FROM customer
WHERE length(customer.product_review) > 200
```

## Without index
```
+-----------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                       |
+-----------------------------------------------------------------------------------------------------------------+
|Seq Scan on customer  (cost=0.00..45305.26 rows=333317 width=212) (actual time=1188.159..1188.160 rows=0 loops=1)|
|  Filter: (length((product_review)::text) > 200)                                                                 |
|  Rows Removed by Filter: 999951                                                                                 |
|Planning Time: 8.387 ms                                                                                          |
|Execution Time: 1188.198 ms                                                                                      |
+-----------------------------------------------------------------------------------------------------------------+
```

## With index
```
+---------------------------------------------------------------------------------------------------------------+
|QUERY PLAN                                                                                                     |
+---------------------------------------------------------------------------------------------------------------+
|Seq Scan on customer  (cost=0.00..45305.26 rows=333317 width=212) (actual time=693.051..693.051 rows=0 loops=1)|
|  Filter: (length((product_review)::text) > 200)                                                               |
|  Rows Removed by Filter: 999951                                                                               |
|Planning Time: 1.021 ms                                                                                        |
|Execution Time: 693.080 ms                                                                                     |
+---------------------------------------------------------------------------------------------------------------+
```