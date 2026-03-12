# pylint: disable=missing-module-docstring

import logging
import os
from datetime import date, timedelta

import duckdb
import streamlit as st

import init_db

if "data" not in os.listdir():
    print("creating folder data")
    logging.error(os.listdir())
    logging.error("creating folder data")
    os.mkdir("data")

if "exercises_sql_tables.duckdb" not in os.listdir("data"):
    exec(open("init_db.py").read())
    # subprocess.run(["python", "init_db.py"])

con = duckdb.connect(database="data/exercises_sql_tables.duckdb", read_only=False)
list_themes = set(init_db.data["theme"])


def check_user_solution(user_query: str) -> None:
    """
    Checks that user's SQL query is correct by:
    1: checking the columns
    2: checking the values
    :param user_query: containing the query inserted by the user
    :return:
    """
    result = con.execute(user_query).df()
    st.dataframe(result)

    try:
        result = result[solution_df.columns]
        st.dataframe(result.compare(solution_df))
        if result.compare(solution_df).shape == (0, 0):
            st.write("Correct, well done!")
            st.balloons()
    except KeyError as e:
        st.write("Some columns are missing")

    n_lines_difference = result.shape[0] - solution_df.shape[0]
    if n_lines_difference != 0:
        st.write(
            f"result has a {n_lines_difference} lines difference with the solution_df"
        )


with st.sidebar:
    theme = st.selectbox(
        "What would you like to review?",
        list_themes,
        index=None,
        placeholder="Select a theme...",
    )
    st.write("You selected:", theme)

    if theme:
        select_exercice_query = f"SELECT * FROM memory_state WHERE theme = '{theme}'"

    else:
        select_exercice_query = "SELECT * FROM memory_state"

    exercise = (
        con.execute(select_exercice_query)
        .df()
        .sort_values("last_reviewed")
        .reset_index(drop=True)
    )
    st.write(exercise)
    exercise_name = exercise.loc[0, "exercise_name"]

    with open(f"answers/{exercise_name}.sql", "r") as f:
        answer = f.read()

    solution_df = con.execute(answer).df()

st.header("enter your code:")
query = st.text_area(label="Please write your input here", key="user_input")


if query:
    check_user_solution(query)

tab1, tab2 = st.tabs(["Tables", "Solution"])


for n_days in [2, 7, 21]:
    if st.button(f"Revoir dans {n_days} jours"):
        next_review = date.today() + timedelta(days=n_days)
        con.execute(
            f"UPDATE memory_state SET last_reviewed = '{next_review}' WHERE exercise_name = '{exercise_name}'"
        )
        st.rerun()

if st.button("Reset"):
    con.execute(f"UPDATE memory_state SET last_reviewed = '1970-01-01'")
    st.rerun()

with tab1:
    exercise_tables = exercise.loc[0, "tables"]
    for table in exercise_tables:
        st.write(f"table: {table}")
        df_table = con.execute(f"SELECT * FROM '{table}'").df()
        st.dataframe(df_table)
    st.write("expected:")
    st.dataframe(solution_df)

with tab2:
    st.write(answer)
