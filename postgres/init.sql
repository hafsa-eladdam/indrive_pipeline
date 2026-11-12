-- Exécuté une seule fois, au premier démarrage de Postgres.
-- 3 couches = 3 schémas.
CREATE SCHEMA raw;      -- données telles qu'elles arrivent
CREATE SCHEMA staging;  -- données nettoyées
CREATE SCHEMA mart;     -- tables métier pour les analystes

-- Tables RAW : là où les DAGs déposent les données
CREATE TABLE raw.drivers (
    driver_id   INT,
    driver_name TEXT,
    phone       TEXT,
    city        TEXT,
    rating      NUMERIC,
    joined_date DATE
);

CREATE TABLE raw.vehicles (
    vehicle_id   INT,
    driver_id    INT,
    make         TEXT,
    model        TEXT,
    plate_number TEXT,
    vehicle_type TEXT
);

CREATE TABLE raw.zones (
    zone_id   INT,
    zone_name TEXT,
    city      TEXT
);

-- une ligne = un événement de course
CREATE TABLE raw.rides (
    ride_id         TEXT,
    driver_id       INT,
    pickup_zone_id  INT,
    dropoff_zone_id INT,
    requested_at    TIMESTAMP,
    distance_km     NUMERIC,
    fare_amount     NUMERIC
);