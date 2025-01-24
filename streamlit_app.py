import streamlit as st
from load_data import csv_to_df

st.session_state.df = csv_to_df('books.csv')

st.set_page_config(page_title='Hardcover Dashboard', page_icon='📚')

dataset = st.Page("dashboard/dataset.py", title="Zbiór danych", icon="📚")
visualization = st.Page("dashboard/visualization.py", title="Wizualizacja danych", icon="📊")
interactive = st.Page("dashboard/interactive.py", title="Interaktywna analiza", icon="🔍")
models = st.Page("dashboard/models.py", title="Modele predykcyjne", icon="📈")
info = st.Page("dashboard/info.py", title="Informacje", icon="\u2139\ufe0f")

pg = st.navigation([dataset, visualization, interactive, models, info])
pg.run()
