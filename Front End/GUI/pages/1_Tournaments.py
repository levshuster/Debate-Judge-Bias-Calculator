
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))
import scrape_tournament_info
import scrape_division_info

import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import Table, MetaData


st.set_page_config(layout="wide")
conn = st.connection("postgresql", type="sql")
metadata = MetaData()
tournament_table = Table('tournament', metadata, autoload_with=conn.engine)
division_table = Table('division', metadata, autoload_with=conn.engine)

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
	"",
	placeholder="https://www.tabroom.com/index/tourn/index.mhtml?tourn_id=...",
	# on_change=update
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
			label="I this information is correct and would like to upload this tournament the central database",
			on_click=upload_tournament()
		)
		st.markdown(f"[Report with this tournament by sending a bug report email containing the issue and URL](mailto:shusterlev@gmail.com)")

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
