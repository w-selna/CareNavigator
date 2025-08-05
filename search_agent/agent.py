import requests

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from bs4 import BeautifulSoup
from typing import Union


def get_doctors_list(specialty: str, user_latitude: float, user_longitude: float) -> Union[list[str], str]:
    """
    Retrieve a list of Healthgrades doctor profile URLs based on a medical specialty and geographic location.

    This function sends an HTTP GET request to Healthgrades using the provided medical specialty and
    latitude/longitude coordinates, then parses the returned HTML to extract links to individual
    doctor profiles. Only results from the first page are returned.

    Args:
        specialty (str): The medical specialty to search for (e.g., "Oncology", "Pediatrics").
        user_latitude (float): The latitude coordinate of the search location.
        user_longitude (float): The longitude coordinate of the search location.

    Returns:
        list[str]: A list of URLs to individual doctor profile pages on Healthgrades.
        str: An error message string if the request or parsing fails.

    Notes:
        - This function parses static HTML. If the site content is rendered dynamically via JavaScript,
          the results may be incomplete or empty.
        - The structure of Healthgrades pages may change, which could break this scraper.
        - Currently, only the first page of results is retrieved. Pagination is not handled.
    """
    doctor_urls = []

    base_url = (
        f'https://www.healthgrades.com/usearch?what={specialty}'
        f'&pt={user_latitude}%2C{user_longitude}&sort.provider=bestmatch'
    )
    print(f"[DEBUG] Requesting URL: {base_url}")

    try:
        response = requests.get(
            base_url,
            headers={'User-Agent': 'Mozilla/5.0'},
            cookies={}
        )
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        listings = soup.find_all('div', attrs={'role': 'presentation'})

        for listing in listings:
            link = listing.find('a', href=True)
            if link and 'href' in link.attrs:
                doctor_urls.append(f'https://www.healthgrades.com{link["href"]}')

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        return f'Error on line {tb[-1].lineno}: {e}'

    return doctor_urls


search_agent = Agent(
    model=LiteLlm('openai/gpt-4o'),
    name='search_agent',
    description='Retrieve a list of doctor URLs in a given specialty near a given location to compile the data.',
    instruction="""
    You are a helpful assistant that helps users find doctor profiles in Healthgrades.
    You will be given a medical specialty and a latitude/longitude indicating the user's location.
    Your task is to retrieve a list of URLs to doctor profiles in Healthgrades that are related to the given specialty and near the given location and give the entire list to the user.
    Use the get_doctors_list function to retrieve the list of doctors.
    If the request is outside the scope of finding a doctor profile, politely decline the request.
    '""",
    tools= [get_doctors_list]
)

root_agent = search_agent
