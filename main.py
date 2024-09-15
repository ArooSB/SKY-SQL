import data
from datetime import datetime
import sqlalchemy

SQLITE_URI = "sqlite:///data/flights.sqlite3"
IATA_LENGTH = 3


def delayed_flights_by_airline(data_manager):
    """
    Prompts the user to input an airline name and retrieves the delayed flights associated with that airline.

    Args:
        data_manager (FlightData): An instance of the FlightData class to interact with the database.
    """
    airline_input = input("Enter airline name: ")
    results = data_manager.get_delayed_flights_by_airline(airline_input)
    print_results(results)


def delayed_flights_by_airport(data_manager):
    """
    Prompts the user to input an origin airport IATA code and retrieves the delayed flights associated with that airport.
    The input is validated to ensure it is an alphabetic IATA code of the correct length.

    Args:
        data_manager (FlightData): An instance of the FlightData class to interact with the database.
    """
    valid = False
    while not valid:
        airport_input = input("Enter origin airport IATA code: ")
        if airport_input.isalpha() and len(airport_input) == IATA_LENGTH:
            valid = True
    results = data_manager.get_delayed_flights_by_airport(airport_input)
    print_results(results)


def flight_by_id(data_manager):
    """
    Prompts the user to input a flight ID and retrieves the flight associated with that ID.
    The input is validated to ensure it is an integer.

    Args:
        data_manager (FlightData): An instance of the FlightData class to interact with the database.
    """
    valid = False
    while not valid:
        try:
            id_input = int(input("Enter flight ID: "))
        except Exception:
            print("Try again...")
        else:
            valid = True
    results = data_manager.get_flight_by_id(id_input)
    print_results(results)


def flights_by_date(data_manager):
    """
    Prompts the user to input a date in DD/MM/YYYY format and retrieves the flights associated with that date.
    The input is validated to ensure it matches the expected date format.

    Args:
        data_manager (FlightData): An instance of the FlightData class to interact with the database.
    """
    valid = False
    while not valid:
        try:
            date_input = input("Enter date in DD/MM/YYYY format: ")
            date = datetime.strptime(date_input, "%d/%m/%Y")
        except ValueError as e:
            print("Try again...", e)
        else:
            valid = True
    results = data_manager.get_flights_by_date(date.day, date.month, date.year)
    print_results(results)


def print_results(results):
    """
    Prints the results of a query in a formatted manner. Each result is expected to contain fields for delay, origin airport,
    destination airport, and airline. If a delay exists, it is included in the output.

    Args:
        results (list): A list of results from the database query.
    """
    print(f"Got {len(results)} results.")
    for result in results:
        result = result._mapping
        try:
            delay = int(result.get("DELAY", 0)) if result.get(
                "DELAY") is not None else 0
            origin = result.get("ORIGIN_AIRPORT")
            dest = result.get("DESTINATION_AIRPORT")
            airline = result.get("AIRLINE", "Unknown")
        except (ValueError, sqlalchemy.exc.SQLAlchemyError) as e:
            print("Error showing results: ", e)
            return
        if delay > 0:
            print(
                f"{result['ID']}. {origin} -> {dest} by {airline}, Delay: {delay} Minutes"
            )
        else:
            print(f"{result['ID']}. {origin} -> {dest} by {airline}")


def show_menu_and_get_input():
    """
    Displays a menu of options to the user and prompts for a choice. The user's choice is validated to ensure it corresponds
    to one of the available menu options.

    Returns:
        function: The function corresponding to the user's choice.
    """
    print("Menu:")
    for key, value in FUNCTIONS.items():
        print(f"{key}. {value[1]}")
    while True:
        try:
            choice = int(input("Please choose a number from the menu: "))
            if choice in FUNCTIONS:
                return FUNCTIONS[choice][0]
        except ValueError:
            pass
        print(
            "Invalid input. Please enter a number corresponding to the menu options.")


FUNCTIONS = {
    1: (flight_by_id, "Show flight by ID"),
    2: (flights_by_date, "Show flights by date"),
    3: (delayed_flights_by_airline, "Delayed flights by airline"),
    4: (delayed_flights_by_airport, "Delayed flights by origin airport"),
    5: (quit, "Exit"),
}


def main():
    """
    The main function that initializes the FlightData object and continuously displays the menu, processing the user's choices
    until the user decides to quit.
    """
    data_manager = data.FlightData(SQLITE_URI)
    while True:
        choice_func = show_menu_and_get_input()
        choice_func(data_manager)


if __name__ == "__main__":
    main()
