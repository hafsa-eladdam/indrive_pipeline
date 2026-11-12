DROP TABLE IF EXISTS mart.revenue_by_zone;
CREATE TABLE mart.revenue_by_zone AS
SELECT
    pickup_zone,
    COUNT(*)         AS nb_rides,
    SUM(fare_amount) AS revenue
FROM mart.rides
GROUP BY pickup_zone;