import streamlit as st
import altair as alt
import pandas as pd

"""
# Interaktywna analiza
"""

df = st.session_state.df

"### Wykres punktowy"
@st.cache_data(hash_funcs={pd.DataFrame: id})
def scatter_plot(df, x='pages', y='rating'):
    scatter_plot = alt.Chart(df).mark_circle().encode(
        x=alt.X(x),
        y=alt.Y(y)
    ).properties(
        width=800,
        height=600
    )
    return scatter_plot
df_numeric = df.select_dtypes(include=['number'])
col1, col2 = st.columns(2)
with col1:
    x = st.selectbox('Wybierz zmienną X', df_numeric.columns, index=1)
with col2:
    y = st.selectbox('Wybierz zmienną Y', df_numeric.columns, index=4)
chart = scatter_plot(df_numeric, x, y)
st.altair_chart(chart, use_container_width=True)

"### Popularność zmiennej kategorycznej"
@st.cache_data(hash_funcs={pd.DataFrame: id})
def categorical_variable(df, n=20, column='Genre'):
    genre_counts = df[column].explode().value_counts().nlargest(n).reset_index()
    genre_counts.columns = [column, 'Liczba książek']

    chart = alt.Chart(genre_counts).mark_bar().encode(
        x=alt.X(column, sort='-y'),
        y='Liczba książek'
    ).properties(
        width=800,
        height=500
    )
    return chart

col1, col2 = st.columns(2)
with col1:
    column = st.selectbox('Wybierz zmienną kategoryczną', ['Genre', 'Mood', 'Content Warning', 'Tag'], index=0)
with col2:
    n = st.number_input('Liczba kategorii', min_value=1, max_value=50, value=20)
chart = categorical_variable(df, n, column)
st.altair_chart(chart, use_container_width=True)
