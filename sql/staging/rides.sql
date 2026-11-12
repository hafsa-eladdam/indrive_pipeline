DROP TABLE IF EXISTS staging.rides;
CREATE TABLE staging.rides AS
SELECT DISTINCT
    ride_id,
    driver_id,
    pickup_zone_id,
    dropoff_zone_id,
    requested_at,
    distance_km,
    fare_amount
FROM raw.rides
WHERE fare_amount > 0
  AND driver_id IN (SELECT driver_id FROM raw.drivers);