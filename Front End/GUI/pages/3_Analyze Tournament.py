
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))

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


"# Available Tournaments"
st.write(conn.query("SELECT * FROM Tournament;", ttl=0))

"# Explore a Single Tournament"
selected_tournament_id = st.selectbox(
	label ="Select A Tournament ID to explore",
	options=[i[1] for i in conn.query("SELECT id FROM tournament;", ttl=0).itertuples()]
)
# if selected_tournament_id:
selected_tournament = conn.query(f"SELECT * FROM tournament WHERE id = {selected_tournament_id};", ttl=0)
f"Divisions of {selected_tournament['name'][0]}"
st.dataframe(
	conn.query(f"SELECT * FROM division WHERE tournament = {selected_tournament_id};", ttl=0),
	use_container_width=True
)

votes_in_tournament = conn.query(f'''
	SELECT division_name, round, to_scrape, judge, side, team, id
	FROM pairing.votes
	LEFT JOIN division
	ON division.id = votes.division
	WHERE division.tournament = {selected_tournament_id}
	AND won IS TRUE;
''')
divisions = votes_in_tournament["division_name"].unique()
selected_divisions = st.multiselect(
    "Filter Out Divisions",
    divisions,
	divisions
)

# rounds = votes_in_tournament[votes_in_tournament["division_name"] in selected_divisions]["round"]
filtered_df = votes_in_tournament.loc[votes_in_tournament["division_name"].isin(selected_divisions)]
rounds = filtered_df["round"].unique()
selected_rounds = st.multiselect(
    "Filter Out Rounds",
    rounds,
	rounds,
)
selected_round_ids = filtered_df.loc[filtered_df["round"].isin(selected_rounds)]['id'].unique()

side_bias_tab, gender_bias_tab = st.tabs(["Aff Neg Bias", "Gender Bias"])

with side_bias_tab:
	if selected_round_ids.any():
		df = conn.query(f'''
			SELECT side, count(*) AS wins
			FROM pairing.votes
			WHERE
				tournament = {selected_tournament_id}
				AND division IN ({','.join(map(str, selected_round_ids))})
				AND won IS TRUE
			GROUP BY side
			;
		''', ttl=0)
		# df = (
		# 	df
		# 	.loc[df["division_name"]
		# 	.isin(selected_divisions)]
		# 	.loc[df["round"]
		# 	.isin(selected_rounds)]
		# )
		# df
		st.plotly_chart(px.pie(
			df,
			values='wins',
			names='side',
			title='Number of Affirmative vs Negative Wins'),
			hole=.3
		)
		st.dataframe(
			data=conn.query(f'''
				SELECT side, won, tournament, division, team
					FROM pairing.votes
					WHERE
						tournament = {selected_tournament_id}
						AND division IN ({','.join(map(str, selected_round_ids))});
			''', ttl=0),
			hide_index=False
		)
