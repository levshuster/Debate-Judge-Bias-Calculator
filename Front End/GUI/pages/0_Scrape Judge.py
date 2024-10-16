
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))

import scrape_judge
import scrape_division_info
import scrape_debaters_and_judges

import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import Table, MetaData, select

st.set_page_config(
    page_title="Debate Bias Calc",
    page_icon="🗣",
	layout="wide"
)

conn = st.connection("postgresql", type="sql")
metadata = MetaData()
parent_judge_table = Table('judge', metadata, autoload_with=conn.engine)
division_table = Table('division', metadata, autoload_with=conn.engine)
team_table = Table('team', metadata, schema='pairing', autoload_with=conn.engine)
judge_table = Table('judge', metadata, schema='pairing', autoload_with=conn.engine)
debater_table = Table('debater', metadata, schema='pairing', autoload_with=conn.engine)
votes_table = Table('votes', metadata, schema='pairing', autoload_with=conn.engine)
points_table = Table('speaker_points', metadata, schema='pairing', autoload_with=conn.engine)

"# Tournaments"

"## Judges already in the database"
st.dataframe(
	data=conn.query('SELECT * FROM judge;', ttl=0), # type: ignore
	hide_index=True
)

# Content

"""
## Add Judge

Find the tabroom link that that contains a `judge_id=` field and paste the URL

"""

url = st.text_input(
	"Tabroom URL",
	placeholder="https://www.tabroom.com/index/tourn/postings/judge.mhtml?judge_id=...&tourn_id=...",
	label_visibility="hidden"
)

should_scrape = False
if scrape_judge.validate_judge_url(url):
	st.write("### Do you wish to scrape this page?")
	id = scrape_judge.get_judge_id(url)
	last_scraped_date = conn.query(f'SELECT updated FROM judge WHERE id = {id};', ttl=0)
	already_scraped = len(last_scraped_date) != 0

	scrape_judge.display_judges_tabroom_page(st.container(height=300), url)

	if already_scraped:
		st.write(f"#### This judge is already in the database but may have judged additional rounds since it was last scraped ({last_scraped_date['updated'].dt.date.values[0]}).")

	should_scrape = st.button(
		label="I affirm that this information is correct and would like to upload this judge the central database",
	)
	st.markdown(f"[Report an issue with this tournament by sending a bug report email containing the issue and URL](mailto:shusterlev@gmail.com)")

if should_scrape:
	st.write("# Scraping Judge Details")
	judge_name = scrape_judge.get_judge_name(url)
	with conn.session as session:
		if already_scraped:
			session.execute(
				parent_judge_table\
					.delete()\
					.where(parent_judge_table.c.id==id)
			)
		session.execute(
			parent_judge_table\
				.insert()\
				.values(
					id=id,
					name=judge_name,
					first_name = judge_name.split()[0],
					url=url,
					updated=datetime.now(),
					details='{}',
					to_scrape=True
			)
		)
		session.commit()

	st.dataframe(
		data=conn.query(f'SELECT * FROM judge WHERE id = {id};', ttl=0), # type: ignore
		hide_index=True
	)


	st.write("# Scraping Debaters")

	judge_urls_to_process = conn.query('SELECT url, name FROM judge WHERE to_scrape = TRUE;', ttl=0)
	judge_progress = st.progress(0, "No Judges Have Been Found that Require Further Processing")

	for count, url, name in judge_urls_to_process.itertuples():
		team_urls = scrape_judge.get_team_urls(url)
		judge_progress.progress((count+1)/len(judge_urls_to_process), f"Adding {len(team_urls)} team entries for Processing {name}")
		with conn.session as session:
			for team_url in team_urls:
				# already_in_db = len(conn.query(f"SELECT * FROM pairing.team WHERE url = '{team_url}';", ttl=0)) != 0
				# if not already_in_db:
				session.execute(
					insert(team_table)
					.values(
						url=team_url,
						to_scrape=True
					)
					.on_conflict_do_nothing(index_elements=['url'])
				)

					# session.execute(
					# 	team_table.insert().values(
					# 		url=url,
					# 		to_scrape=True
					# 	)
					# )
			session.execute(
				parent_judge_table\
					.update()\
					.where(parent_judge_table.c.url == url)\
					.values(to_scrape=False)
			)
			session.commit()

	debater_urls_to_process = conn.query(
	"""
		SELECT
			url
		FROM pairing.team
		WHERE to_scrape = TRUE
		;
	""", ttl=0)

	debaters_progress = st.progress(0, "No Debaters Have Been Found that Require Further Processing")
	for count, debater_url in debater_urls_to_process.itertuples():
		debater_names, team_name = scrape_debaters_and_judges.get_debater_and_team_from_url(debater_url)
		if team_name != None or debater_names != []:
			debaters_progress.progress((count+1)/len(debater_urls_to_process), f"Processing {debater_names[0]} from {team_name}")
			with conn.session as session:
				for debater_name in debater_names:
					session.execute(
						debater_table.insert().values(
							name=debater_name,
							school=team_name,
							first_name=debater_name.split()[0],
							team=debater_url,
						)
					)
				session.execute(
					team_table\
						.update()\
						.where(team_table.c.url == debater_url)\
						.values(to_scrape=False)
				)
				session.commit()

	st.write(conn.query("SELECT * FROM pairing.debater;", ttl=0))

	st.write("# Scraping Votes")
	# get all tournament_id from debater_urls_to_process
	# get all judge URLS for this judge+tournament_id
	# create pairing.judge for each url
	# create vote and speaker points for each to_scrape pairing.judge

	st.write("# Scraping Relivant Tournament Details")
	# Scrape tournament for each tournament URL while setting leaf to TRUE
	st.write("# Scraping Division details")
	# scrape divisions for each tournament URL while setting leaf to TRUE
# else:
# 	"Please provide a valid link"
