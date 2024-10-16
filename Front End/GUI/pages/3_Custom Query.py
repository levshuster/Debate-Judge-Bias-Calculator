
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../Helper Functions/Python/')))

import streamlit as st


st.set_page_config(
	page_title="Debate Bias Calc",
	page_icon="🗣",
	layout="wide"
)
conn = st.connection("postgresql", type="sql")
st.image("../../Back End/Database/debate_bias_calc.svg", caption="Database Structure")
prompt = st.chat_input("EX: SELECT * FROM pairing.votes")


if prompt:
	with st.chat_message('✍️'):
		st.code(prompt, language='sql')

	with st.chat_message('📅'):
		st.write(conn.query(prompt, ttl=0))


# user, table =  st.chat_message('✍️'), st.chat_message('📅')
# if prompt:
# 	user.code(prompt, language='sql')
# 	table.write(conn.query(prompt, ttl=0))
