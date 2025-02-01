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

"### Wykres mozaikowy"
@st.cache_data(hash_funcs={pd.DataFrame: id})
def mozaic_plot(agg_data, x_var='Genre', y_var='Mood'):
    mozaic_plot = alt.Chart(agg_data).mark_rect().encode(
    x=f"{x_var}:O",
    y=f"{y_var}:O",
    color='Liczba:Q',
    tooltip=[x_var, y_var, 'Liczba']
    ).properties(
        width=800,
        height=600
    )
    return mozaic_plot

col1, col2 = st.columns(2)
with col1:
    x_var = st.selectbox(f"Wybierz kategorię dla osi OX", ['Genre', 'Mood', 'Content Warning', 'Tag'], index=0)
with col2:
    y_var = st.selectbox(
        f"Wybierz kategorię dla osi OY",
        options=[col for col in ['Genre', 'Mood', 'Content Warning', 'Tag'] if col != x_var],
        index=1, 
        key="y_var"
    )

df_explode = df.copy()
df_explode[x_var] = df_explode[x_var].apply(lambda x: x if isinstance(x, list) else [x])
df_explode[y_var] = df_explode[y_var].apply(lambda x: x if isinstance(x, list) else [x])
df_explode = df_explode.dropna(subset=[x_var, y_var])
df_explode = df_explode.explode(x_var).explode(y_var)
agg_data = df_explode.groupby([x_var, y_var]).size().reset_index(name="Liczba")
agg_data = agg_data[agg_data[x_var].isin(df_explode[x_var].unique()) & agg_data[y_var].isin(df_explode[y_var].unique())]
# Wybór liczby pokazywanych kategorii
x_unique = df_explode[x_var].nunique()
st.info(f"Max liczba kategorii do wyboru to {x_unique}, w zależności od liczby unikalnych kategorii na osi X.")
top_n = st.number_input("Wybierz liczbę top kategorii", min_value=1, max_value=x_unique, value=20, step=1)
top_x = agg_data.groupby(x_var)['Liczba'].sum().nlargest(top_n).index
top_y = agg_data.groupby(y_var)['Liczba'].sum().nlargest(top_n).index
agg_data= agg_data[agg_data[x_var].isin(top_x) & agg_data[y_var].isin(top_y)]

chart = mozaic_plot(agg_data, x_var, y_var)
st.altair_chart(chart, use_container_width=True)