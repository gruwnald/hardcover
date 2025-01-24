import streamlit as st
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from sklearn.metrics import mean_squared_error
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.multioutput import MultiOutputRegressor

"# Modele predykcyjne"

df = st.session_state.df

columns = st.multiselect('Wybierz kolumny do modelowania', 
                         ['ratings_count', 'release_year',
                          'pages', 'editions_count', 'lists_count',
                          'journals_count', 'reviews_count', 'Genre',
                          'Mood', 'Content Warning', 'Tag'],
                         default=['ratings_count', 'release_year',
                                  'pages', 'editions_count', 'lists_count',
                                  'journals_count', 'reviews_count', 'Genre',
                                  'Mood', 'Content Warning', 'Tag'])
if not columns:
    st.write("Wybierz co najmniej jedną kolumnę")
    st.stop()

@st.cache_resource(hash_funcs={pd.DataFrame: id})
def prepare_data(df):
    df = df[['rating', 'ratings', 'ratings_count', 'release_year',
            'pages', 'editions_count', 'lists_count',
            'journals_count', 'reviews_count', 'Genre',
            'Mood', 'Content Warning', 'Tag']].dropna()
    top_values = {
        'Genre': df['Genre'].explode().value_counts().nlargest(50).index,
        'Mood': df['Mood'].explode().value_counts().nlargest(15).index,
        'Content Warning': df['Content Warning'].explode().value_counts().nlargest(5).index,
        'Tag': df['Tag'].explode().value_counts().nlargest(5).index
    }
    for column, top in top_values.items():
        df[column] = df[column].apply(lambda x: [i if i in top else column+'_inne' for i in x])

    df['rating_var'] = df.apply(
        lambda x: sum(
            count * (rating - x.rating) ** 2 
            for rating, count in x.ratings.items()
        ) / (x.ratings_count - 1), axis=1)
    df = df.drop(columns=["ratings"])

    df = df[['rating', 'rating_var'] + columns]
    mlb = MultiLabelBinarizer()
    for column in top_values.keys():
        if column in columns:
            df = df.join(pd.DataFrame(mlb.fit_transform(df[column]), columns=mlb.classes_, index=df.index))
    df = df.drop(columns=[col for col in ['Genre', 'Mood', 'Content Warning', 'Tag'] if col in columns])
    
    X = df.drop(columns=['rating', 'rating_var'], axis=1).astype("float32").to_numpy()
    y = df[['rating', 'rating_var']].astype("float32").to_numpy()
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=314)
    return X_train, X_test, y_train, y_test, df.columns.drop(['rating', 'rating_var'])

X_train, X_test, y_train, y_test, train_columns = prepare_data(df)

"## Regresja liniowa"

@st.cache_resource(hash_funcs={np.ndarray: id})
def linear_regression(X_train, X_test, y_train, y_test):
    model_rating = LinearRegression()
    model_rating.fit(X_train, y_train[:, 0])

    model_rating_var = LinearRegression()
    model_rating_var.fit(X_train, y_train[:, 1])

    y_pred_rating = model_rating.predict(X_test)
    mse_rating = mean_squared_error(y_test[:, 0], y_pred_rating)
    y_pred_rating_var = model_rating_var.predict(X_test)
    mse_rating_var = mean_squared_error(y_test[:, 1], y_pred_rating_var)

    def sum_coefficients(coef, numeric_cols, columns):
        coef_sum = {}
        for column in ('Genre', 'Mood', 'Content Warning', 'Tag'):
            if column in columns:
                coef_sum[column] = coef.filter(like=column).sum()
        for column in numeric_cols:
            coef_sum[column] = coef[column]
        return pd.Series(coef_sum)

    coef_rating = pd.Series(model_rating.coef_, index=train_columns)
    coef_rating_var = pd.Series(model_rating_var.coef_, index=train_columns)
    numeric_cols = ['release_year', 'pages', 'editions_count', 'lists_count', 'journals_count', 'reviews_count']
    numeric_cols = [col for col in numeric_cols if col in columns]
    coef_sum_rating = sum_coefficients(coef_rating, numeric_cols, columns).sort_values(ascending=False)
    coef_sum_rating_var = sum_coefficients(coef_rating_var, numeric_cols, columns).sort_values(ascending=False)
    coef_sum_rating.name = 'Współczynnik'
    coef_sum_rating_var.name = 'Współczynnik'

    return mse_rating, mse_rating_var, coef_sum_rating, coef_sum_rating_var

mse_rating, mse_rating_var, coef_sum_rating, coef_sum_rating_var = linear_regression(X_train, X_test, y_train, y_test)

f"""
Błąd średniokwadratowy dla średniej oceny: **{mse_rating:.4f}**  
Błąd średniokwadratowy dla wariancji ocen: **{mse_rating_var:.4f}**
"""

"**Współczynniki regresji:**"
col1, col2 = st.columns(2)
with col1:
    "Współczynniki dla średniej oceny"
    st.write(coef_sum_rating)
with col2:
    "Współczynniki dla wariancji ocen"
    st.write(coef_sum_rating_var)

"## Gradient Boosting"
@st.cache_resource(hash_funcs={np.ndarray: id})
def gradient_boosting(X_train, X_test, y_train, y_test):
    model = MultiOutputRegressor(GradientBoostingRegressor())
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    mse_rating = mean_squared_error(y_test[:, 0], y_pred[:, 0])
    mse_rating_var = mean_squared_error(y_test[:, 1], y_pred[:, 1])
    return mse_rating, mse_rating_var

mse_rating, mse_rating_var = gradient_boosting(X_train, X_test, y_train, y_test)

f"""
Błąd średniokwadratowy dla średniej oceny: **{mse_rating:.4f}**  
Błąd średniokwadratowy dla wariancji ocen: **{mse_rating_var:.4f}**
"""
