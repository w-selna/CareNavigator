from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

#WS Edit: Lots to fix here

def search_flights(from_airport : str, to_airport : str, date_of_flight : str) -> dict:
    """
    Searches for available flights between two airports on a specified date.

    Args:
        from_airport (str): The IATA code or name of the departure airport.
        to_airport (str): The IATA code or name of the destination airport.
        date_of_flight (str): The date of the flight in 'YYYY-MM-DD' format.
    Returns:
        dict: A dictionary containing a list of available flights, where each flight is represented as a dictionary with keys:
            - 'flight_number' (str): The flight's unique identifier.
            - 'from' (str): The departure airport.
            - 'to' (str): The destination airport.
            - 'date' (str): The date of the flight.
            - 'price' (float): The price of the flight.
    """


    return {
        "flights": [
            {
                "flight_number": "AB123",
                "from": from_airport,
                "to": to_airport,
                "date": date_of_flight,
                "price": 199.99
            },
            {
                "flight_number": "CD456",
                "from": from_airport,
                "to": to_airport,
                "date": date_of_flight,
                "price": 299.99
            }
        ]
    }

flight_search_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='flight_search_agent',
    description='An agent that helps with searching for flights.',
    instruction='Use the available tools to search for flights.',
    tools=[search_flights]
)
