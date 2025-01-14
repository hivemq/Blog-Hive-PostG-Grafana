CREATE TABLE IF NOT EXISTS tempdata (
    id SERIAL PRIMARY KEY,
    isotime TIMESTAMPTZ,
    unixtime BIGINT,   -- Unix timestamp in seconds
    SensorID TEXT,
    temperature float
);


