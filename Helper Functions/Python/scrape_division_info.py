import scrape_tournament_info
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from sqlalchemy import and_
import urllib



def parse_division_name(tournament_url, table, session):
	tournament_id = scrape_tournament_info.get_id_from_url(tournament_url)
	divisions = scrape_tournament_info.get_formats(tournament_url)
	if len(divisions) == 0:
		st.write(f"No division found for {tournament_url}")
		return
	division_progress = st.progress(0, f"Processing {divisions[0][1]}")
	division_count = 1
	for id, division_name in divisions:
		parse_events(id, division_name, tournament_id, table, session)
		division_progress.progress(division_count/len(divisions), f"Finished Processing {division_name}")
		division_count += 1
	division_progress.empty()


def parse_events(event_id, division_name, tournament_id, table, session):
	response = requests.post(
		"https://www.tabroom.com/index/tourn/postings/index.mhtml",
		data={
			'tourn_id': tournament_id,
			'event_id': event_id
		}
	)
	pattern = r"/index/tourn/postings/round\.mhtml\?tourn_id="+tournament_id+r"&round_id=\d+"
	urls = set('https://www.tabroom.com'+match for match in re.findall(pattern, response.text))
	for url in urls: parse_rounds(division_name, tournament_id, url, table, session)

def parse_rounds(division_name, tournament_id, url, table, session):
	id = int(url.split("=")[-1])
	response = requests.get(url)
	round = BeautifulSoup(response.text, 'html.parser')\
		.find_all('h4')[-1]\
		.get_text(strip=True)

	with session as session:
		session.execute(
			table\
				.delete()\
				.where(and_(
					table.c.id == id,
					table.c.tournament == tournament_id,
				))
		)
		session.execute(
			table\
				.insert()\
				.values(
					id=id,
					tournament=tournament_id,
					division_name = division_name,
					format = '',
					level = '',
					round = round,
					is_elimination = None,
					url=url,
					details='{}',
					to_scrape=True
			)
		)
		session.commit()

def get_team_and_judge_urls_from_division(url):
	team_urls,judge_urls = [], []

	# Send a GET request to the URL
	response = requests.get(url)

	# Check if the request was successful
	if response.status_code == 200:
		soup = BeautifulSoup(response.text, 'html.parser')
		links = soup.find_all('a')

		# Loop through all found <a> tags
		for link in links:
			href = link.get('href')  # Get the href attribute of each <a> tag
			if href:  # If href exists, add it to the list of URLs
				full_url = urllib.parse.urljoin(url, href) # type: ignore
				if 'entry_record' in full_url:
					team_urls.append(full_url)
				elif 'judge.mhtml' in full_url:
					judge_urls.append(full_url)
	else:
		print(f"Failed to retrieve the page. Status code: {response.status_code}")
	return set(team_urls), set(judge_urls)
