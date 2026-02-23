import streamlit as st
import pandas as pd
import duckdb

#con = duckdb.connect(":default:")

st.write("Hello World, this is the dataframe 'df'")
data = {"a": [1, 2, 3], "b": [4, 5, 6] }
df = pd.DataFrame(data)
st.dataframe(df)


sql_query = st.text_area(label="Please write your input here")
result = duckdb.query(sql_query)
st.write(f"You submitted the following query '{sql_query}'")
st.dataframe(result)


