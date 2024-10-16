
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))
import scrape_judge

from bs4 import BeautifulSoup
import requests
import streamlit as st
import plotly.express as px


st.set_page_config(
	page_title="Debate Bias Calc",
	page_icon="🗣",
	layout="wide"
)
conn = st.connection("postgresql", type="sql")


"# Available Judges"
st.write(conn.query("SELECT * FROM pairing.judge;", ttl=0))

"# Explore a Single Judge"
selected_judge_id = st.selectbox(
	label ="Select A Judge ID to explore",
	options=[i[1] for i in conn.query("SELECT id FROM pairing.judge;", ttl=0).itertuples()]
)
selected_judge = conn.query(f"SELECT * FROM pairing.judge WHERE id = {selected_judge_id};", ttl=0)

st.write(selected_judge)
url = selected_judge["url"][0]

side_bias_tab, gender_bias_tab, tabroom_tab = st.tabs(["Aff Neg Bias", "Gender Bias", "Tabroom"])


with tabroom_tab:
	scrape_judge.display_judges_tabroom_page(st, url)

with side_bias_tab:
	df = conn.query(f'''
		SELECT side, count(*) AS wins
		FROM pairing.votes
		WHERE
			judge = {selected_judge_id}
			AND won IS TRUE
		GROUP BY side
		;
	''', ttl=0)
	st.plotly_chart(px.pie(
		df,
		values='wins',
		names='side',
		title='Number of Affirmative vs Negative Wins'),
		hole=.3
	)
	st.dataframe(
		data=conn.query(f'SELECT side, won, tournament, division, team FROM pairing.votes WHERE judge = {selected_judge_id};', ttl=0),
		hide_index=True
	)
