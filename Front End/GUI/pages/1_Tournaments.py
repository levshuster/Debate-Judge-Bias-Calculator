
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))

import scrape_tournament_info
import streamlit as st
import pandas as pd
from datetime import datetime
from sqlalchemy import Table, MetaData


st.set_page_config(layout="wide")
conn = st.connection("postgresql", type="sql")

"# Tournaments already in DB"
st.dataframe(
	data=conn.query('SELECT * FROM tournament;', ttl=0), # type: ignore
	hide_index=True
)

# Content

"""
# Add Tournament

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
	already_in_db = len(conn.query(f'SELECT * FROM tournament WHERE id = {id};', ttl=0)) == 0

	if already_in_db:
		"This Tournament is Not Already in the Database"
	else:
		"This tournament is already in the Database but you may update it"

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
		metadata = MetaData()
		tournament_table = Table('tournament', metadata, autoload_with=conn.engine)
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
	st.markdown(f"[Report an but processing this tournament by emailing me the error and URL](mailto:shusterlev@gmail.com)")


else:
	"Please provide a valid link"
