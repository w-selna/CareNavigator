import aiohttp
import json
import re
import requests

from google.adk.agents.llm_agent import Agent
from google.adk.models.lite_llm import LiteLlm
from bs4 import BeautifulSoup
from typing import Union, Dict, Any


def get_doctors_list(specialty: str, latitude: float, longitude: float, page : int = 1) -> Union[list[str], str]:
    """
    Retrieve a list of Healthgrades doctor profile URLs based on a medical specialty and geographic location.

    This function sends an HTTP GET request to Healthgrades using the provided medical specialty and
    latitude/longitude coordinates, then parses the returned HTML to extract links to individual
    doctor profiles. Only results from the first page are returned.

    Args:
        specialty (str): The medical specialty to search for (e.g., "Oncology", "Pediatrics").
        latitude (float): The latitude of the search location.
        longitude (float): The longitude of the search location.
        page (int): The page number of the search results to retrieve.

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
        f'&pt={latitude}%2C{longitude}&pageNum={page}&sort.provider=bestmatch'
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

    return doctor_urls[:10]


def parse_doctor_information(url: str) -> Union[Dict[str, Any], str]:
    """
    Parse detailed doctor profile information from a Healthgrades profile page.

    This function retrieves a Healthgrades doctor profile page and extracts key details,
    including the doctor's name, specialty, years of experience, biography, address,
    frequently treated conditions, procedures, rating, review count, accepted insurance,
    and whether the doctor is currently accepting new patients.

    Args:
        url (str): Full URL to the doctor's profile page on Healthgrades.

    Returns:
        dict: A dictionary containing the parsed doctor profile information with keys:
            - name (str): Full name of the doctor.
            - url (str): Profile URL.
            - specialty (str): Listed medical specialty.
            - experience (str): Years of experience (or 'not listed').
            - bio (str): Biography text.
            - address (str): Office address.
            - conditions (list[str]): Conditions the doctor frequently treats.
            - procedures (list[str]): Procedures the doctor performs.
            - insurance_data (list[dict] or None): Parsed insurance plan information, if available.
            - score (str): Rating score from Healthgrades.
            - qty_reviews (str): Total number of reviews.
            - accepting_new_patients (bool): Whether the doctor is accepting new patients.

        str: An error message containing the exception details and line number if parsing fails.

    Notes:
        - This function assumes a stable HTML structure for Healthgrades profiles.
          If the structure changes, selectors may need updates.
        - Some elements may not exist on every profile (e.g., biography, years of experience).
        - The insurance data is extracted from embedded JavaScript and may require adjustments
          if Healthgrades changes its data storage format.
    """
    try:
        response = requests.get(
            url,
            headers={'User-Agent': 'Mozilla/5.0'},
            cookies={}
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')

        # Doctor name
        name = soup.find('h1', class_='summary-provider-name').text.strip()

        # Specialty
        specialty = soup.find('div', class_='speciality-name-text').text.replace('*', '').strip()

        # Years of experience
        try:
            experience = soup.find('div', class_='years-of-experience-text').text.split(' ')[0].replace('+', '').strip()
            experience = f'{experience} years'
        except AttributeError:
            experience = 'not listed'

        # Biography
        bio = soup.find('p', attrs={'data-qa-target': 'premium-biography'}).text.strip()

        # Address
        address = soup.find('address').text.strip()

        # Conditions
        conditions = [
            condition.split(':')[-1].strip()
            for condition in soup.find('meta', attrs={'name': 'conditions'})['content'].split(',')
        ]

        # Procedures
        procedures = [
            procedure.split(':')[-1].strip()
            for procedure in soup.find('meta', attrs={'name': 'procedures'})['content'].split(',')
        ]

        # Review score and quantity
        score = soup.find('span', class_='score').text.strip()
        qty_reviews = soup.find('span', class_='review-summary-horizontal-scroll__content').text.split(' ')[0].strip()

        # Insurance data (from embedded script)
        insurance_script = soup.find_all('script')[6]
        insurance_data = None
        for script in insurance_script.string.split('HG3.profile.pageState || ')[1].split(';'):
            if 'insuranceAccepted' in script:
                insurance_data = dict(json.loads(script))['providerProfileModel']['insuranceAccepted']
                break

        # Accepting new patients (from utag_data script)
        script = soup.find('script', string=re.compile(r'utag_data'))
        raw_js = script.string
        pattern = re.compile(r"utag_data\['(.*?)'\]\s*=\s*\"(.*?)\";")
        utag_dict = dict(pattern.findall(raw_js))
        accepting_new_patients = utag_dict.get('AcceptNewPatients') == 'yes'

        return {
            'name': name,
            'url': url,
            'specialty': specialty,
            'experience': experience,
            'bio': bio,
            'address': address,
            'conditions': conditions,
            'procedures': procedures,
            'insurance_data': insurance_data,
            'score': score,
            'qty_reviews': qty_reviews,
            'accepting_new_patients': accepting_new_patients
        }

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        return f'Error on line {tb[-1].lineno}: {e}'



search_agent = Agent(
    model=LiteLlm('openai/gpt-4o'),
    name='search_agent',
    description='Retrieve a list of doctor URLs in a given specialty near a given location to compile the data.',
    instruction="""
    You are a helpful assistant that helps users find doctor profiles in Healthgrades.
    You will be given a medical specialty and a latitude/longitude indicating the user's location.
    Your task is to retrieve a list of doctors from Healthgrades that are related to the given specialty and near the given location.
    From this list, visit each doctor profile to summarize their information.
    Then, give the entire list of doctors and summaries to the user.
    Any follow-on questions about the doctor should be answered by the information in their profile.
    Use the get_doctors_list function to retrieve the list of doctors.
    Use the parse_doctor_information function to retrieve the information about a specific doctor from their profile.
    If the request is outside the scope of finding a doctor profile, politely decline the request.
    """,
    tools= [get_doctors_list, parse_doctor_information]
)

root_agent = search_agent
