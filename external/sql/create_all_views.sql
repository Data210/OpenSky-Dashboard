CREATE OR REPLACE VIEW flight_time_by_airport AS
select a.airport, AVG((lastseen-firstseen)/60) as tim, COUNT(*)
from public.flight as f
JOIN public.airport as a On f.estDepartureAirport = a.icao
GROUP BY (a.airport)
HAVING COUNT(*) > 10
ORDER BY (tim) DESC


CREATE OR REPLACE VIEW total_flight_time_num_flights_distance_per_aircraft AS
select f.icao24, SUM((lastseen-firstseen)/(60*60)) as tim, COUNT(*) as total, FLOOR(SUM(calculate_distance(a1.latitude, a1.longitude, a2.latitude, a2.longitude, 'K'))) AS total_distance
from public.flight as f
JOIN airport as a1 on f.estDepartureAirport = a1.icao
JOIN airport as a2 on f.estArrivalAirport = a2.icao
WHERE FLOOR((calculate_distance(a1.latitude, a1.longitude, a2.latitude, a2.longitude, 'K'))) > 0
GROUP BY (f.icao24)
ORDER BY tim DESC,total_distance DESC


CREATE VIEW total_flights as
SELECT COUNT(*) from flight


CREATE VIEW flight_hours as
select SUM((lastseen-firstseen)/(60*60)) as tim
from public.flight as f


CREATE VIEW grouped_stats AS
SELECT *
FROM total_flights
CROSS JOIN
flight_hours
CROSS JOIN 
total_unique_aircraft
CROSS JOIN
total_flight_distance


CREATE OR REPLACE VIEW most_popular_operator_by_country AS
select DISTINCT ON (country) operator, country, iso3, count(*) as total
from public.flight as f
JOIN public.aircraft as a ON f.icao24 = a.icao24
JOIN public.operator as o ON o.operator_id = a.operator_id
JOIN public.country as c ON o.country_id = c.country_id
where o.operator_id != 0 and o.operator != 'NaN'
GROUP BY (operator, country, iso3)
ORDER BY country ASC, total DESC


CREATE VIEW total_flight_distance AS
SELECT FLOOR(SUM(calculate_distance(a1.latitude, a1.longitude, a2.latitude, a2.longitude, 'K'))) AS total_distance
FROM flight as f
JOIN airport as a1 on f.estDepartureAirport = a1.icao
JOIN airport as a2 on f.estArrivalAirport = a2.icao


CREATE VIEW total_unique_aircraft AS
SELECT COUNT(DISTINCT icao24) as total_aircraft
FROM flight as f


CREATE VIEW all_airports AS
select airport, type, iso, longitude, latitude
from airport as a
JOIN country as c on a.country_id = c.country_id


CREATE OR REPLACE VIEW popular_routes AS
select a.airport as "Departure", a2.airport as "Arrival", a.longitude as "dep_lon", a.latitude as "dep_lat", a2.longitude as "arr_lon", a2.latitude as "arr_lat", AVG((lastseen-firstseen)/60) as tim, COUNT(*)
from public.flight as f
JOIN public.airport as a On f.estDepartureAirport = a.icao
JOIN public.airport as a2 ON f.estarrivalAirport = a2.icao
WHERE a.icao != a2.icao
GROUP BY (a.airport, a2.airport, a.longitude, a.latitude, a2.longitude, a2.latitude)
HAVING COUNT(*) > 1 AND AVG((lastseen-firstseen)/60) > 60
ORDER BY (Count(*)) DESC
LIMIT 100


CREATE VIEW all_routes AS
select a.airport as "Departure", a2.airport as "Arrival", a.longitude as "dep_lon", a.latitude as "dep_lat", a2.longitude as "arr_lon", a2.latitude as "arr_lat", AVG((lastseen-firstseen)/60) as tim, COUNT(*)
from public.flight as f
JOIN public.airport as a On f.estDepartureAirport = a.icao
JOIN public.airport as a2 ON f.estarrivalAirport = a2.icao
WHERE a.icao != a2.icao
GROUP BY (a.airport, a2.airport, a.longitude, a.latitude, a2.longitude, a2.latitude)


CREATE OR REPLACE VIEW most_popular_route_by_country as
select DISTINCT ON (c.country) c.country as "Departure Country", c2.country as "Arrival Country", COUNT(*) as total
from public.flight as f
JOIN public.airport as a On f.estDepartureAirport = a.icao
JOIN public.country as c ON a.country_id = c.country_id
JOIN public.airport as a2 ON f.estarrivalAirport = a2.icao
JOIN public.country as c2 ON a2.country_id = c2.country_id
WHERE c.country != c2.country
GROUP BY (c.country, c2.country)
HAVING COUNT(*) > 1
ORDER BY c.country DESC, total DESC


CREATE VIEW most_popular_route_by_country_ordered AS
select * from most_popular_route_by_country
ORDER BY total DESC


CREATE OR REPLACE VIEW flights_with_weekday AS
SELECT *, To_Char(date_trunc('day', to_timestamp(firstseen)), 'Day') AS week_day, extract(isodow from to_timestamp(firstseen)) as week_day_num
FROM public.flight


CREATE OR REPLACE VIEW total_flights_per_day AS
SELECT week_day, COUNT(*),week_day_num
FROM flights_with_weekday
GROUP BY(week_day, week_day_num)
ORDER BY week_day_num ASC


CREATE VIEW total_flight_time_per_day AS
SELECT week_day, SUM((lastseen-firstseen)/3600)
FROM flights_with_weekday
GROUP BY(week_day)


CREATE VIEW flight_time_by_country AS
select country, AVG((lastseen-firstseen)/60) as tim
from public.flight as f
JOIN public.airport as a ON f.estDepartureAirport = a.icao
JOIN public.country as c ON a.country_id = c.country_id
GROUP BY (country)
ORDER BY (tim) DESC


CREATE OR REPLACE VIEW flights_by_manufacturer AS
select manufacturer, COUNT(*) as total
from public.flight as f
JOIN public.aircraft as a ON f.icao24 = a.icao24
where manufacturer != 'NaN' AND manufacturer != 'Null'
GROUP BY (manufacturer)
ORDER BY (total) DESC


CREATE OR REPLACE VIEW flights_by_country AS
select iso3, count(*) as total
from public.flight as f
JOIN public.aircraft as a ON f.icao24 = a.icao24
JOIN public.operator as o ON o.operator_id = a.operator_id
JOIN public.country as c ON o.country_id = c.country_id
where o.operator_id != 0 and o.operator != 'NaN'
GROUP BY (country,iso3)
ORDER BY total DESC


CREATE OR REPLACE VIEW flights_by_operator AS
select operator, count(*)
from public.flight as f
JOIN public.aircraft as a ON f.icao24 = a.icao24
JOIN public.operator as o ON o.operator_id = a.operator_id
where o.operator_id != 0 and o.operator != 'NaN'
GROUP BY (operator)
ORDER BY COUNT(*) DESC


CREATE VIEW flights_by_operator_country as
select operator, country, count(*) as total
from public.flight as f
JOIN public.aircraft as a ON f.icao24 = a.icao24
JOIN public.operator as o ON o.operator_id = a.operator_id
JOIN public.country as c ON o.country_id = c.country_id
where o.operator_id != 0 and o.operator != 'NaN'
GROUP BY (operator, country)


CREATE VIEW flight_time_by_operator AS
select operator, AVG((lastseen-firstseen)/60) as tim, count(*)
from public.flight as f
JOIN public.aircraft as a ON f.icao24 = a.icao24
JOIN public.operator as o ON o.operator_id = a.operator_id
where o.operator_id != 0 and o.operator != 'NaN'
GROUP BY (operator)
HAVING count(*) > 5
ORDER BY (tim) DESC


CREATE OR REPLACE VIEW total_flights_arriving_by_airport as
select airport, count(*) as total, iso
from public.flight as f
JOIN public.airport as ap ON f.estarrivalairport = ap.icao
JOIN public.country as c ON ap.country_id = c.country_id
GROUP BY (airport, iso)
ORDER BY total DESC


CREATE OR REPLACE VIEW total_flights_departing_by_airport as
select airport, count(*) as total, iso
from public.flight as f
JOIN public.airport as ap ON f.estDepartureAirport = ap.icao
JOIN public.country as c ON ap.country_id = c.country_id
GROUP BY (airport, iso)
ORDER BY total DESC


-- domestic vs international
CREATE OR REPLACE VIEW routes_with_iso3 as
select a.airport as "Departure", a2.airport as "Arrival", c1.iso3 as "dep_iso3", c2.iso3 as "arr_iso3"
from public.flight as f
JOIN public.airport as a On f.estDepartureAirport = a.icao
JOIN public.country as c1 ON a.country_id = c1.country_id
JOIN public.airport as a2 ON f.estarrivalAirport = a2.icao
JOIN public.country as c2 ON a2.country_id = c2.country_id
-- GROUP BY (a.airport, a2.airport)


CREATE VIEW longest_flight AS
select a1.airport as "dep_airport", a2.airport as "arr_airport", c1.iso as "dep_iso", c2.iso as "arr_iso", FLOOR(MAX(calculate_distance(a1.latitude, a1.longitude, a2.latitude, a2.longitude, 'K'))) as "dist" from flight as f
JOIN public.airport as a1 On f.estDepartureAirport = a1.icao
JOIN public.country as c1 ON a1.country_id = c1.country_id
JOIN public.airport as a2 ON f.estarrivalAirport = a2.icao
JOIN public.country as c2 ON a2.country_id = c2.country_id
GROUP BY (a1.airport, a2.airport, c1.iso, c2.iso)
ORDER BY "dist" DESC
LIMIT 1


CREATE VIEW domestic_vs_international_flights as
SELECT t_top.c1 as "Domestic", j_top.c1 as "International"
FROM
(select SUM(t.count) as c1
FROM 
(select dep_iso3, arr_iso3, COUNT(*)
from routes_with_iso3
GROUP BY (dep_iso3, arr_iso3)) AS t
WHERE t.dep_iso3 = t.arr_iso3) AS t_top
CROSS JOIN
(select SUM(t.count) as c1
FROM 
(select dep_iso3, arr_iso3, COUNT(*)
from routes_with_iso3
GROUP BY (dep_iso3, arr_iso3)) AS t
WHERE t.dep_iso3 != t.arr_iso3) as j_top