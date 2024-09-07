import streamlit as st
import pandas as pd

conn = st.connection("postgresql", type="sql")


# Perform query.
df = conn.query('SELECT * FROM tournament;', ttl="10m")
df
