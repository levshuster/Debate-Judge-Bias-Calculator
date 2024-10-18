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
			response.raise_for_status()
			soup = BeautifulSoup(response.text, 'html.parser')

			# Find and remove the <header> tag if it exists
			header = soup.find('header')
			if header:
				soup = header.extract()  # Remove the header tag and its contents

			# Find and remove navigation bar
			tabs = soup.find('ul', id='tabnav') # type: ignore
			if tabs:
				tabs.extract()
			else: print("no tabnav found")


			menu = soup.find(class_='main') # type: ignore
			if menu:
				soup = menu.extract()

			st.html(str(soup))

		except requests.exceptions.RequestException as e:
			st.error(f"An error occurred: {e}")


def get_judge_name(url):
	response = requests.get(url)
	# response.raise_for_status()  # Check for request errors
	soup = BeautifulSoup(response.text, 'html.parser')
	header = soup.find('h3')
	if header != None:
		return (
			header
			.text
			.strip()
			.lower()
		)
	else:
		return "No Name Found"

def get_team_urls(url):
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	return set(
		'https://www.tabroom.com'+link.get('href')
		for link in soup.find_all('a')
		if link.get('href') if 'postings/entry_record' in link.get('href')
	)


# get_team_urls('https://www.tabroom.com/index/tourn/postings/judge.mhtml?judge_id=1985775&tourn_id=26620')

def get_tournament_ids_from_judge(url):
	soup = BeautifulSoup(requests.get(url).text, 'html.parser')
	return set(
		link.get('href').split('tourn_id=')[-1].split('&')[0]
		for link in soup.find_all('a')
		if link.get('href') if 'tourn_id=' in link.get('href')
	)

# print(get_tournament_ids_from_judge('https://www.tabroom.com/index/tourn/postings/judge.mhtml?judge_id=2118573&tourn_id=29348'))

