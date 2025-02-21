import streamlit as st

pg = st.navigation([
    st.Page("lab14.py", title="Lab14"),
    st.Page("lab13.py", title="Lab 13"),
    st.Page("lab9-10.py", title="Lab 9-12"),
    st.Page("lab5_8.py", title="Lab 5-8"), 
    st.Page("exercise4.py", title="Exercise 4"), 
    st.Page("exercise3.py", title="Exercise 3"), 
    st.Page("lab3-4.py", title="Lab 3-4"),
])
pg.run()