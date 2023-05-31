CREATE TABLE States (
    icao24 VARCHAR(30),
    callsign VARCHAR(30),
    origin_country VARCHAR(255),
    last_contact INT,
    longitude REAL,
    latitude REAL,
    baro_altitude REAL,
    on_ground BOOLEAN,
    velocity REAL,
    true_track REAL,
    vertical_rate REAL,
    geo_altitude REAL
);