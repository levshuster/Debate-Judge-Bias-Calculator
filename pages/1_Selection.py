import streamlit as st

st.set_page_config(
    page_title="DJBC - Selection", 
    page_icon="🗣️", 
    layout="wide", 
    initial_sidebar_state="collapsed",
)

st.title("DJBC - Selection")

left, middle, right = st.columns(3)
with left:
    st.write("""
    ## Upload an existing .bias file
    ---
    """)
    a = st.file_uploader(label="Upload a .bias file", type=["bias"])
    
    
with middle:
    st.write("""
    ## Generate a new .bias file
    **Warning:** this can take up to half an hour
    
    Why? to create a new judge record, we need to visit two tabroom webpages for every round the judge has every seen. This is a lot of webpages, and takes a while to load.
    
    ---
    
    """)
    
with right:
    st.write("""
    ## Use our example file
    
    ---
    
   """)

