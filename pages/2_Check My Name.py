import streamlit as st

st.set_page_config(
    page_title="DJBC - Check My Name", 
    page_icon="🗣️", 
    layout="wide", 
    initial_sidebar_state="auto",
)

st.title("DJBC - Check My Name")

"""
## Can DJBC correctly guess your gender from your name?
"""
name = st.text_input("Enter your first name", autocomplete="given-name", placeholder='EX Alex')# .to_lower()
"""
---

### DJBC polls an API of 2 Million names. 

Is your name in the API? Is your name cashed by DJBC? What is the confidence of the guess? Try entering your name!

---

### We at DBML reconginse the issues with guessing name's genders to identify bias such as

- Less common names are less likely to be in the API 
- the API makes no attempt to equally represent names of different cultures
- this tool doesn't consider names that are often used by multiple genders

We included this tool in an effort to be transparent about the limitations of our tool. We hope to improve this tool in the future.

This page is also helpful for determining a reasonable confidance threashold (try entering a name like 'alex' to see how our confidence falls with name common to multiple genders)

---

"""

