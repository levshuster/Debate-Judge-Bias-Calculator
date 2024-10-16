from bs4 import BeautifulSoup
import requests

def get_judge_id(judge_url:str):
	try:
		return judge_url.split("judge_id=")[1].split('&')[0]
	except:
		return None

def validate_judge_url(judge_url:str):
	return get_judge_id(judge_url) != None

def display_judges_tabroom_page(st, url):
	if url:
		try:
			response = requests.get(url)
			response.raise_for_status()  # Check for request errors
			soup = BeautifulSoup(response.text, 'html.parser')
			# Find and remove the <header> tag if it exists
			header = soup.find('header')
			if header:
				soup = header.extract()  # Remove the header tag and its contents

			tabs = soup.find('ul', id='tabnav')
			if tabs:
				tabs.extract()
			else: print("no tabnav found")

			# menu = soup.find(class_='sidenote')
			menu = soup.find(class_='main')
			if menu:
				soup = menu.extract()

			st.html(str(soup))

		except requests.exceptions.RequestException as e:
			st.error(f"An error occurred: {e}")
