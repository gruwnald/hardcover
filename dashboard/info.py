import streamlit as st

"""
# Informacje

## Autorzy
- **Krzysztof Mizgała**
- **Jerzy Grunwald**
- **Kamil Kordek**

## Opis

Aplikacja pozwala na analizę zbioru danych dotyczącego książek.  
Zbiór danych zawiera informacje o książkach, takie jak:  
1. `id` - unikalny identyfikator książki
2. `title` - tytuł książki
3. `description` - opis książki
4. `rating` - średnia ocena książki
5. `ratings` - rozkład ocen
6. `ratings_count` - liczba ocen
7. `release_year` - rok wydania książki
8. `pages` - liczba stron
9. `users_count` - liczba użytkowników, którzy ocenili książkę
10. `reviews_count` - liczba recenzji
11. `editions_count` - liczba wydań
12. `lists_count` - liczba pojawień się książki w listach użytkowników
13. `journals_count` - liczba pojawień się książki w czasopismach
14. `Genre` - gatunek
15. `Mood` - nastrój książki
16. `Pace` - tempo książki
17. `Tag` - tagi (pozostałe istotne cechy książki)
18. `Content Warning` - ostrzeżenia o drażliwych treściach
19. `Member` - członek społeczności, który dodał książkę

Każda ze zmiennych jakościowych kodowana jest jako lista napisów, aby książka mogła należeć jednocześnie do kilku kategorii.  
Do analizy obliczamy dodatkowo wariancję ocen.

## Cel

Celem aplikacji jest analiza zbioru danych dotyczącego książek.  
Analiza obejmuje:  
- wyświetlenie wykresów
- filtrowanie danych
- wyświetlenie statystyk

Pytania badawcze, na które chcemy odpowiedzieć:  
- Jakie cechy mają największy wpływ na ocenę książki przez czytelnika?
- Co wpływa na spójność ocen?
- Czy istnieją korelacje pomiędzy zmiennymi?

## Wykorzystane technologie

- Python
- Streamlit
- Numpy i Pandas
- Matplotlib i Altair
- Scikit-learn
- Keras i TensorFlow
"""
