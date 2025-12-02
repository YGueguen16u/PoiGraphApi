-- Basic POI query

SELECT
    p.poi_id AS "POI Id",
    p.poi_name AS "POI Name" ,
    p.lat AS "Latitude",
    p.long AS "Longitude",
    c.city_name AS "City Name",
    cat.category_name AS "Category Name"
FROM poi AS p
LEFT JOIN city AS c ON p.city_id = c.city_id
LEFT JOIN category AS cat ON p.category_id = cat.category_id
LIMIT 50;