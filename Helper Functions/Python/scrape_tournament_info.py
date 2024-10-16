import requests
from bs4 import BeautifulSoup
import re

def url_is_in_exspected_format(url):
	return re.fullmatch(r'https://www\.tabroom\.com/index/tourn/postings/index\.mhtml\?tourn_id=\d+', url) != None

def get_id_from_url(url):
	return url.split('=')[-1]

def get_tournament_name_from_url(url):
	response = requests.get(url)
	soup = BeautifulSoup(response.text, 'html.parser')
	first_h2 = soup.find('h2')
	if first_h2:
		return first_h2.get_text(strip=True)
	else:
		return "No Title Found"

def get_formats(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    first_dropdown = soup.find('select')
    if first_dropdown:
        return [
            (option.get('value'), option.text.strip())
            for option in first_dropdown.find_all('option')[1:] # type: ignore
        ]
    else:
        return [None, "No Options Found"]
