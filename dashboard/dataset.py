import streamlit as st

"""
# Zbiór danych
## Filtry
"""

df = st.session_state.df

df['rating_var'] = df.apply(
    lambda x: sum(
        count * (rating - x.rating) ** 2 
        for rating, count in x.ratings.items()
    ) / (x.ratings_count - 1), axis=1)
df = df.drop(columns=["ratings"])

col1, col2 = st.columns(2)
with col1:
    rating_filter = st.slider('Średnia ocena',
                              min_value=0.0,
                              max_value=5.0,
                              value=(0.0, 5.0))
    min_year = st.number_input('Minimalny rok wydania',
                               min_value=int(df['release_year'].min()),
                               max_value=int(df['release_year'].max()),
                               value=int(df['release_year'].min()))
    max_year = st.number_input('Maksymalny rok wydania',
                               min_value=int(df['release_year'].min()),
                               max_value=int(df['release_year'].max()),
                               value=int(df['release_year'].max()))
    count_filter = st.slider('Liczba ocen',
                             min_value=0,
                             max_value=df.ratings_count.max(),
                             value=(0, df.ratings_count.max()))

with col2:
    std_filter = st.slider('Wariancja ocen',
                           min_value=df.rating_var.min(),
                           max_value=df.rating_var.max(),
                           value=(df.rating_var.min(), df.rating_var.max()))
    min_pages = st.number_input('Minimalna liczba stron',
                                min_value=int(df['pages'].min()),
                                max_value=int(df['pages'].max()),
                                value=int(df['pages'].min()))
    max_pages = st.number_input('Maksymalna liczba stron',
                                min_value=int(df['pages'].min()),
                                max_value=int(df['pages'].max()),
                                value=int(df['pages'].max()))
    title_filter = st.text_input('Szukaj tytułu książki', '')

genre_filter = st.multiselect('Wybierz gatunki', df['Genre'].explode().unique(), default=('Fantasy'))

filtered_df = df[
    (df['rating'] >= rating_filter[0]) & (df['rating'] <= rating_filter[1]) &
    (df['rating_var'] >= std_filter[0]) & (df['rating_var'] <= std_filter[1]) &
    (df['ratings_count'] >= count_filter[0]) & (df['ratings_count'] <= count_filter[1]) &
    (df['pages'] >= min_pages) & (df['pages'] <= max_pages) &
    (df['release_year'] >= min_year) & (df['release_year'] <= max_year) &
    (df['Genre'].apply(lambda x: any(item in x for item in genre_filter))) &
    (df['title'].str.contains(title_filter, case=False))
]

cols = df.columns
selected_cols = st.multiselect('Wybierz kolumny do wyświetlenia', cols,
    default=['title', 'rating', 'rating_var', 'ratings_count', 'pages', 'users_count', 'Genre'])

filtered_df[selected_cols]
