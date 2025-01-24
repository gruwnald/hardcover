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
