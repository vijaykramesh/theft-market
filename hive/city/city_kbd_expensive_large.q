SELECT t2.city, t2.state_code, t2.average, t2.sum_num_listings 
FROM (
  SELECT t1.city, t1.state_code, sum(t1.num_listings) as sum_num_listings, round(avg(t1.price)) as average
  FROM (
    SELECT city, state_code, price, num_listings
    FROM city_avg_list
    WHERE num_bed=1 and week_ending_date BETWEEN '2010-01-01' and '2010-12-31'
  ) t1
  GROUP BY t1.city, t1.state_code
  ORDER BY average ASC
) t2
WHERE t2.sum_num_listings > 5000
ORDER BY t2.average DESC
LIMIT 10;