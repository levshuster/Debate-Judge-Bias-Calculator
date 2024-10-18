
import sys
import os
import time

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))

import scrape_tournament_info
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
tournament_table = Table('tournament', metadata, autoload_with=conn.engine)
division_table = Table('division', metadata, autoload_with=conn.engine)
team_table = Table('team', metadata, schema='pairing', autoload_with=conn.engine)
judge_table = Table('judge', metadata, schema='pairing', autoload_with=conn.engine)
debater_table = Table('debater', metadata, schema='pairing', autoload_with=conn.engine)
votes_table = Table('votes', metadata, schema='pairing', autoload_with=conn.engine)
points_table = Table('speaker_points', metadata, schema='pairing', autoload_with=conn.engine)

"# Tournaments"

"## Tournaments already in the database"
st.dataframe(
	data=conn.query('SELECT * FROM tournament;', ttl=0), # type: ignore
	hide_index=True
)

# Content

"""
## Add Tournament

Find the tabroom link that looks roughly like
`https://www.tabroom.com/index/tourn/postings/index.mhtml?tourn_id=26620`
and enter it below:

"""

# def update():
# 	st.write(scrape_tournament_info.url_is_in_exspected_format(url))


url = st.text_input(
	"Tabroom URL",
	placeholder="https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=...",
	label_visibility="hidden"
)


if scrape_tournament_info.url_is_in_exspected_format(url):
	id = scrape_tournament_info.get_id_from_url(url)
	name = scrape_tournament_info.get_tournament_name_from_url(url)
	already_in_db = len(conn.query(f'SELECT * FROM tournament WHERE id = {id};', ttl=0)) != 0

	if already_in_db:
		"This tournament is already in the Database"
	else:
		st.dataframe(
			data=pd.DataFrame({
				'id': [id],
				'name': [name],
				'url': [url],
				'updated': [datetime.now()],
			}),
			hide_index=True
		)

		"The divisions are:"

		st.dataframe(
			data=pd.DataFrame(scrape_tournament_info.get_formats(url)),
			hide_index=True
		)

		def upload_tournament():
			with conn.session as session:
				session.execute(
					tournament_table\
						.delete()\
						.where(tournament_table.c.id==id)
				)
				session.execute(
					tournament_table\
						.insert()\
						.values(
							id=id,
							name=name,
							url=url,
							updated=datetime.now(),
							details='{}',
							to_scrape=True
					)
				)
				session.commit()


		st.button(
			label="I affirm that this information is correct and would like to upload this tournament the central database",
			on_click=upload_tournament()
		)
		st.markdown(f"[Report an issue with this tournament by sending a bug report email containing the issue and URL](mailto:shusterlev@gmail.com)")

else:
	"Please provide a valid link"

"# Divisions"

tournament_urls_to_process = conn.query('SELECT url, name FROM tournament WHERE to_scrape = TRUE;', ttl=0)


tournament_progress = st.progress(0, "No Tournaments Have Been Found that Require Further Processing")
for tournament in tournament_urls_to_process.itertuples():
	tournament_progress.progress((tournament[0])/len(tournament_urls_to_process), f"Processing Tournament {tournament[2]}")

	scrape_division_info.parse_division_name(
		tournament_url=tournament[1],
		table = division_table,
		session = conn.session
	)
	tournament_progress.progress(1.0, "Finished Processing Tournaments")
	with conn.session as session:
		session.execute(
			tournament_table\
				.update()\
				.where(tournament_table.c.url == tournament[1])\
				.values(to_scrape=False)
		)
		session.commit()

st.dataframe(
	data=conn.query('SELECT * FROM division;', ttl=0), # type: ignore
	hide_index=True
)

"# Pairings"

division_urls_to_process = conn.query(
"""
	SELECT
		round,
		tournament,
		url
	FROM division
	WHERE
		to_scrape = TRUE
		AND url <> ''
	;
""", ttl=0)
# 		AND (
# 			division_name LIKE '%LD%'
# 			division_name LIKE '%Lincoln%'
# 			OR division_name LIKE '%Public%'
# 			OR division_name LIKE '%CX%'
# 		)
# 	;
# """, ttl=0) #TODO make better IE filter than just checking if

# "# Skipped Rounds:"
# st.write(conn.query(
# """
# 	SELECT
# 		*
# 	FROM division
# 	WHERE to_scrape = TRUE AND url NOT IN (
# 		SELECT
# 			url
# 		FROM division
# 		WHERE
# 			to_scrape = TRUE
# 			AND url <> ''
# 			AND (
# 				division_name LIKE '%LD%'
# 				OR division_name LIKE '%Public%'
# 				OR division_name LIKE '%CX%'
# 				OR division_name LIKE '%Policy%'
# 				OR division_name LIKE '%Lincoln%'
# 			)
# 	)
# 	;
# """, ttl=0))

division_progress = st.progress(0, "No Divisions Have Been Found that Require Further Processing")
for count, round, tournament, division_url in division_urls_to_process.itertuples():
	division_progress.progress((count+1)/len(division_urls_to_process), f"Processing Division {round} from tournament {tournament}")
	team_urls,judge_urls = scrape_division_info.get_team_and_judge_urls_from_division(division_url)
	with conn.session as session:
		for url in team_urls:
			result = session.execute(
				select(team_table.c.url).where(team_table.c.url == url)
			).fetchone()
			if result is None:
				session.execute(
					team_table.insert().values(
						url=url,
						to_scrape=True
					)
				)
		for url in judge_urls:
			result = session.execute(
				select(judge_table.c.url).where(judge_table.c.url == url)
			).fetchone()
			if result is None:
				session.execute(
					judge_table.insert().values(
						url=url,
						to_scrape=True,
						id=url.split("judge_id=")[-1].split("&")[0]
					)
				)

		session.execute(
			division_table\
				.update()\
				.where(division_table.c.url == division_url)\
				.values(to_scrape=False)
		)
		session.commit()


# st.write(conn.query("SELECT * FROM pairing.team;", ttl=0))
# st.write(conn.query("SELECT * FROM pairing.judge;", ttl=0))

"# Debaters"
debater_urls_to_process = conn.query(
"""
	SELECT
		url
	FROM pairing.team
	WHERE to_scrape = TRUE
	;
""", ttl=0)

debater_urls_to_process

debaters_progress = st.progress(0, "No Debaters Have Been Found that Require Further Processing")
for count, debater_url in debater_urls_to_process.itertuples():
	debater_names, team_name = scrape_debaters_and_judges.get_debater_and_team_from_url(debater_url)
	if team_name != None and debater_names != []:
		debaters_progress.progress((count+1)/len(debater_urls_to_process), f"Processing {debater_names[0]} from {team_name}")
		with conn.session as session:
			for debater_name in debater_names:
				session.execute(
					debater_table.insert().values(
						name=debater_name,
						school=team_name,
						first_name=lower(debater_name.split()[0]),
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

"# Judges"
st.write(conn.query("SELECT * FROM pairing.judge;", ttl=0))

judge_urls_to_process = conn.query("SELECT url FROM pairing.judge WHERE to_scrape = TRUE;", ttl=0)

judges_progress = st.progress(0, "No Judges Have Been Found that Require Further Processing")
warnings = st.expander("See Exceptions", icon='⚠️')
for count, judges_url in judge_urls_to_process.itertuples():
	judges_progress.progress((count+1)/len(judge_urls_to_process), f"Processing {judges_url}")
	votes, speaker_points = scrape_debaters_and_judges.get_votes_and_speaker_points_for_a_tournament_from_judge_url(warnings, judges_url)
	with conn.session as session:
		for vote in votes:
			session.execute(
				votes_table.insert().values(
					judge=vote.judge_id,
					team=vote.team_link,
					division=vote.division_id,
					tournament=vote.tourn_id,
					won=vote.won,
					side=vote.side
				)
			)
		for point in speaker_points:
			session.execute(
				points_table.insert().values(
					judge=point.judge_id,
					team=point.team_link,
					partial_name=point.name,
					division=point.division_id,
					tournament=point.tourn_id,
					value=point.points,
				)
			)
		session.execute(
			judge_table\
				.update()\
				.where(judge_table.c.url == judges_url)\
				.values(to_scrape=False)
		)
		session.commit()

st.write(conn.query("SELECT * FROM pairing.votes;", ttl=0))
st.write(conn.query("SELECT * FROM pairing.speaker_points;", ttl=0))
