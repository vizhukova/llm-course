import streamlit as st

pg = st.navigation([
    st.Page("lab5.py", title="Lab 5"), 
    st.Page("exercise4.py", title="Exercise 4"), 
    st.Page("exercise3.py", title="Exercise 3"), 
    st.Page("lab3-4.py", title="Lab 3-4"),
])
pg.run()