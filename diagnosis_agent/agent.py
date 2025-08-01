from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

#WS Edit: Lots to fix here.

def diagnosis_agent(flight_number: str, from_airport: str, to_airport: str, date_of_flight: str) -> dict:
    """
    Books a flight with the specified details.

    Args:
        flight_number (str): The flight number to book.
        from_airport (str): The IATA code of the departure airport.
        to_airport (str): The IATA code of the destination airport.
        date_of_flight (str): The date of the flight in 'YYYY-MM-DD' format.

    Returns:
        dict: A dictionary containing the flight booking details with keys 'flight_number', 'from', 'to', 'date', and 'Airline confirmation'.
    """

    return {
        "flight_number": flight_number,
        "from": from_airport,
        "to": to_airport,
        "date": date_of_flight,
        "Airline confirmation": "CFKAKLQ12",
    }

flight_booking_agent = Agent(
    model=LiteLlm(model="openai/gpt-4o"),
    name='flight_booking_agent',
    description='An agent that helps with booking flights.',
    instruction='Assist users in booking flights based on user input.',
    tools=[diagnosis_agent]
)

