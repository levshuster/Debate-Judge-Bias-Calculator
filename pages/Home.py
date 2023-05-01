import streamlit as st

st.set_page_config(
    page_title="DJBC", 
    page_icon="🗣️", 
    layout="wide", 
    initial_sidebar_state="expanded")

st.title("DJBC")

st.write("""
## Welcome to Debate Judge Bias Calculator

A tool to quantify signs of bias in debate judges

---
### How to use
Go to the upload page to upload or generate a debate file, then select the results page to view the results.
""")