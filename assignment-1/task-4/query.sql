SELECT COUNT(CASE
                 WHEN "rental_date" < "return_date" THEN 1
             END) as LATE,
       COUNT(CASE
                 WHEN "rental_date" = "return_date" THEN 1
             END) as ON_TIME,
       COUNT(CASE
                 WHEN "return_date" is null THEN 1
             END) as HAVE_NOT_BEEN_RETURNED
FROM "rental"