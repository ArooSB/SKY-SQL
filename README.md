Queries Overview

1. Basic Flight Information by ID

SELECT
ID AS id,
YEAR AS year,
MONTH AS month,
DAY AS day,
ORIGIN_AIRPORT AS origin,
DESTINATION_AIRPORT AS destination,
DEPARTURE_DELAY AS delay
FROM
flights
WHERE
ID = 280;

Certainly! Below is a README.md file that explains each of the SQL queries you've provided.

Flight Data Analysis - SQL Queries
This document provides an overview of various SQL queries used to analyze flight data. Each query is explained in detail, including its purpose and what information it extracts from the database.

Queries Overview

1. Basic Flight Information by ID
   sql
   Copy code
   SELECT
   ID AS id,
   YEAR AS year,
   MONTH AS month,
   DAY AS day,
   ORIGIN_AIRPORT AS origin,
   DESTINATION_AIRPORT AS destination,
   DEPARTURE_DELAY AS delay
   FROM
   flights
   WHERE
   ID = 280;

2. Detailed Flight Information by ID with Airline Name

SELECT
f.ID AS id,
f.YEAR AS year,
f.MONTH AS month,
f.DAY AS day,
f.ORIGIN_AIRPORT AS origin,
f.DESTINATION_AIRPORT AS destination,
a.AIRLINE AS airline_name,
f.DEPARTURE_DELAY AS delay
FROM
flights f
JOIN
airlines a ON f.AIRLINE = a.ID
WHERE
f.ID = 280;

3. Top 5 Flights with the Longest Total Delay

SELECT
ID,
YEAR,
MONTH,
DAY,
DAY_OF_WEEK,
AIRLINE,
FLIGHT_NUMBER,
ORIGIN_AIRPORT,
DESTINATION_AIRPORT,
DEPARTURE_DELAY,
ARRIVAL_DELAY,
(DEPARTURE_DELAY + ARRIVAL_DELAY) AS TOTAL_DELAY
FROM
flights
ORDER BY
TOTAL_DELAY DESC
LIMIT 5;

Certainly! Below is a README.md file that explains each of the SQL queries you've provided.

Flight Data Analysis - SQL Queries
This document provides an overview of various SQL queries used to analyze flight data. Each query is explained in detail, including its purpose and what information it extracts from the database.

Queries Overview

1. Basic Flight Information by ID
   sql
   Copy code
   SELECT
   ID AS id,
   YEAR AS year,
   MONTH AS month,
   DAY AS day,
   ORIGIN_AIRPORT AS origin,
   DESTINATION_AIRPORT AS destination,
   DEPARTURE_DELAY AS delay
   FROM
   flights
   WHERE
   ID = 280;
   Purpose:
   This query retrieves basic information about a specific flight, identified by its ID. The information includes the flight's date (year, month, day), origin and destination airports, and the departure delay. In this case, the flight with ID = 280 is selected.

2. Detailed Flight Information by ID with Airline Name
   sql
   Copy code
   SELECT
   f.ID AS id,
   f.YEAR AS year,
   f.MONTH AS month,
   f.DAY AS day,
   f.ORIGIN_AIRPORT AS origin,
   f.DESTINATION_AIRPORT AS destination,
   a.AIRLINE AS airline_name,
   f.DEPARTURE_DELAY AS delay
   FROM
   flights f
   JOIN
   airlines a ON f.AIRLINE = a.ID
   WHERE
   f.ID = 280;
   Purpose:
   This query extends the previous one by also including the airline's name (airline_name) for the specified flight. It joins the flights table with the airlines table on the airline's ID and fetches additional information about the airline operating the flight.

3. Top 5 Flights with the Longest Total Delay
   sql
   Copy code
   SELECT
   ID,
   YEAR,
   MONTH,
   DAY,
   DAY_OF_WEEK,
   AIRLINE,
   FLIGHT_NUMBER,
   ORIGIN_AIRPORT,
   DESTINATION_AIRPORT,
   DEPARTURE_DELAY,
   ARRIVAL_DELAY,
   (DEPARTURE_DELAY + ARRIVAL_DELAY) AS TOTAL_DELAY
   FROM
   flights
   ORDER BY
   TOTAL_DELAY DESC
   LIMIT 5;
   Purpose:
   This query identifies the top 5 flights with the longest combined delay (departure delay + arrival delay). The query orders the flights by the total delay in descending order and limits the result to the top 5.

4. Top 10 Airports by Number of Departures

   SELECT
   ORIGIN_AIRPORT AS airport,
   COUNT(\*) AS total_departures
   FROM
   flights
   GROUP BY
   ORIGIN_AIRPORT
   ORDER BY
   total_departures DESC
   LIMIT 10;

5. Average Total Delay by Airline

SELECT
a.AIRLINE AS airline,
AVG(f.DEPARTURE_DELAY + f.ARRIVAL_DELAY) AS average_delay
FROM
flights f
JOIN
airlines a ON f.AIRLINE = a.ID
GROUP BY
a.AIRLINE
ORDER BY
average_delay DESC;

6. Average Delay by Airline (Considering Only Positive Delays)

SELECT
a.AIRLINE AS airline,
AVG(CASE
WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY
ELSE 0
END + CASE
WHEN f.ARRIVAL_DELAY > 0 THEN f.ARRIVAL_DELAY
ELSE 0
END) AS average_delay
FROM
flights f
JOIN
airlines a ON f.AIRLINE = a.ID
GROUP BY
a.AIRLINE
ORDER BY
average_delay DESC;

7. Airports with the Most Flights and Highest Average Delay

WITH FlightCounts AS (
SELECT
ORIGIN_AIRPORT,
COUNT(_) AS num_of_flights
FROM
flights
GROUP BY
ORIGIN_AIRPORT
HAVING
COUNT(_) > 5000
),
AverageDelays AS (
SELECT
f.ORIGIN_AIRPORT,
AVG(CASE
WHEN f.DEPARTURE_DELAY > 0 THEN f.DEPARTURE_DELAY
ELSE 0
END + CASE
WHEN f.ARRIVAL_DELAY > 0 THEN f.ARRIVAL_DELAY
ELSE 0
END) AS average_delay
FROM
flights f
JOIN
FlightCounts fc ON f.ORIGIN_AIRPORT = fc.ORIGIN_AIRPORT
GROUP BY
f.ORIGIN_AIRPORT
)
SELECT
a.AIRPORT AS airport,
fc.num_of_flights,
ad.average_delay
FROM
AverageDelays ad
JOIN
FlightCounts fc ON ad.ORIGIN_AIRPORT = fc.ORIGIN_AIRPORT
JOIN
airports a ON fc.ORIGIN_AIRPORT = a.IATA_CODE
ORDER BY
average_delay DESC;
