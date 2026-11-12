DROP TABLE IF EXISTS mart.driver_leaderboard;
CREATE TABLE mart.driver_leaderboard AS
SELECT
    r.driver_id,
    r.driver_name,
    v.vehicle_type,
    COUNT(*)           AS nb_rides,
    SUM(r.fare_amount) AS revenue
FROM mart.rides r
JOIN staging.vehicles v ON v.driver_id = r.driver_id
GROUP BY r.driver_id, r.driver_name, v.vehicle_type;