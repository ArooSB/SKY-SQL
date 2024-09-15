from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError

# Define SQL queries
QUERY_FLIGHT_BY_ID = """
SELECT flights.*, airlines.airline AS AIRLINE, flights.ID as FLIGHT_ID, 
       flights.DEPARTURE_DELAY as DELAY 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE flights.ID = :id AND flights.DEPARTURE_DELAY IS NOT NULL AND flights.DEPARTURE_DELAY >= 0
"""

QUERY_DELAYED_FLIGHTS_BY_AIRLINE = """
SELECT flights.*, airlines.airline AS AIRLINE 
FROM flights 
JOIN airlines ON flights.airline = airlines.id 
WHERE airlines.airline LIKE :airline 
AND flights.DEPARTURE_DELAY IS NOT NULL 
AND flights.DEPARTURE_DELAY > 20
"""

QUERY_DELAYED_FLIGHTS_BY_AIRPORT = """
SELECT * FROM flights 
WHERE ORIGIN_AIRPORT = :airport 
AND DEPARTURE_DELAY IS NOT NULL 
AND DEPARTURE_DELAY > 20
"""

QUERY_FLIGHTS_BY_DATE = """
SELECT * FROM flights 
WHERE DAY = :day AND MONTH = :month AND YEAR = :year
"""

QUERY_DELAYED_FLIGHTS_PER_ROUTE = """
SELECT ORIGIN_AIRPORT, DESTINATION_AIRPORT, 
       AVG(DEPARTURE_DELAY > 20) * 100 AS PERCENT_DELAY 
FROM flights 
WHERE DEPARTURE_DELAY IS NOT NULL 
AND DEPARTURE_DELAY > 20 
GROUP BY ORIGIN_AIRPORT, DESTINATION_AIRPORT
"""


class FlightData:
    """
    The FlightData class provides an interface to the flight data in the SQLite database.
    """

    def __init__(self, db_uri):
        """
        Initialize the connection to the SQLite database.

        Args:
            db_uri (str): The database URI.
        """
        self._engine = create_engine(db_uri)

    def _execute_query(self, query, params):
        """
        Execute an SQL query with the params provided in a dictionary,
        and return a list of records (dictionary-like objects).

        Args:
            query (str): The SQL query to be executed.
            params (dict): The parameters to be used in the query.

        Returns:
            list: A list of records fetched from the database.
        """
        try:
            with self._engine.connect() as connection:
                result = connection.execute(text(query), params)
                return result.fetchall()
        except SQLAlchemyError as e:
            print(f"Error executing query: {e}")
            return []

    def get_flight_by_id(self, flight_id):
        """
        Search for flight details using flight ID.

        Args:
            flight_id (int): The ID of the flight to be retrieved.

        Returns:
            list: A list with a single record of the flight details.
        """
        params = {"id": flight_id}
        return self._execute_query(QUERY_FLIGHT_BY_ID, params)

    def get_delayed_flights_by_airline(self, airline_name):
        """
        Get delayed flights for a specific airline.

        Args:
            airline_name (str): The name of the airline.

        Returns:
            list: A list of delayed flights for the specified airline.
        """
        params = {"airline": f"%{airline_name}%"}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRLINE, params)

    def get_delayed_flights_by_airport(self, airport_code):
        """
        Get delayed flights from a specific origin airport.

        Args:
            airport_code (str): The IATA code of the origin airport.

        Returns:
            list: A list of delayed flights for the specified origin airport.
        """
        params = {"airport": airport_code}
        return self._execute_query(QUERY_DELAYED_FLIGHTS_BY_AIRPORT, params)

    def get_flights_by_date(self, day, month, year):
        """
        Get flights for a specific date.

        Args:
            day (int): The day of the date.
            month (int): The month of the date.
            year (int): The year of the date.

        Returns:
            list: A list of flights for the specified date.
        """
        params = {"day": day, "month": month, "year": year}
        return self._execute_query(QUERY_FLIGHTS_BY_DATE, params)

    def get_delayed_flights_per_route(self):
        """
        Get the percentage of delayed flights per route.

        Returns:
            list: A list of routes with the percentage of delayed flights.
        """
        return self._execute_query(QUERY_DELAYED_FLIGHTS_PER_ROUTE, {})

    def __del__(self):
        """
        Dispose of the database engine when the object is destroyed.
        """
        self._engine.dispose()
