import streamlit as st
import pandas as pd
import duckdb


st.write("""
# SQL SRS
Spaced Repetition System SQL practice
""")

with st.sidebar:
    option = st.selectbox("What would you like to review?",
                      ["Joins", "GroupBy", "Window Functions"],
                      index=None,
                      placeholder="Select a theme..."
                    )
    st.write("You selected:", option)

data = {"a": [1, 2, 3], "b": [4, 5, 6] }
df = pd.DataFrame(data)
st.dataframe(df)


sql_query = st.text_area(label="Please write your input here")
result = duckdb.query(sql_query)
st.write(f"You submitted the following query '{sql_query}'")
st.dataframe(result)


