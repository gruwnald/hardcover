import streamlit as st
import altair as alt
import pandas as pd

"# Wizualizacja danych"

df = st.session_state.df

"### Rozkład ocen książek"
@st.cache_data(hash_funcs={pd.DataFrame: id})
def rozklad_ocen(df):
    ratings = df['ratings'].apply(lambda x: x.keys()).explode()
    ratings_counts = ratings.value_counts().reset_index()
    ratings_counts.columns = ['Ocena', 'Liczba książek']

    chart = alt.Chart(ratings_counts).mark_bar().encode(
        x=alt.X('Ocena:O', sort=alt.EncodingSortField(field='Ocena', order='ascending')),
        y='Liczba książek:Q'
    ).properties(
        width=800,
        height=400
    )
    return chart
chart = rozklad_ocen(df)
st.altair_chart(chart, use_container_width=True)

"### Rozkład liczby stron"
@st.cache_data(hash_funcs={pd.DataFrame: id})
def rozklad_liczby_ocen(df, maxbins=50, log_scale=True):
    chart = alt.Chart(df).mark_bar().encode(
        alt.X('pages:Q', bin=alt.Bin(maxbins=maxbins), title='Liczba stron'),
        alt.Y('count()', title='Liczba książek',
              scale=alt.Scale(type='log' if log_scale else 'linear'))
    ).properties(
        width=800,
        height=400
    )
    return chart
col1, col2 = st.columns(2)
with col1:
    maxbins = st.slider('Liczba przedziałów', min_value=1, max_value=100, value=50)
with col2:
    log_scale = st.checkbox('Skala logarytmiczna', value=True)
chart = rozklad_liczby_ocen(df, maxbins=maxbins, log_scale=log_scale)
st.altair_chart(chart, use_container_width=True)

"### Średnia ocena w zależności od roku wydania"
@st.cache_data(hash_funcs={pd.DataFrame: id})
def get_release_year(x):
    avg_rating_by_year = df.groupby('release_year')['rating'].mean().reset_index()
    line_chart = alt.Chart(avg_rating_by_year).mark_line().encode(
        x=alt.X('release_year:O', scale=alt.Scale(zero=False), title='Rok wydania'),
        y=alt.Y('rating:Q', scale=alt.Scale(zero=False), title='Średnia ocena')
    ).properties(
        width=800,
        height=400
    )
    return line_chart
chart = get_release_year(df)
st.altair_chart(chart, use_container_width=True)
