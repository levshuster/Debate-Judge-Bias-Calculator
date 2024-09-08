import scrape_tournament_info
import requests
import re
from bs4 import BeautifulSoup
import pandas as pd
import streamlit as st
from sqlalchemy import and_


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
