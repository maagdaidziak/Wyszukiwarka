import altair as alt
import pandas as pd
import re
import collections
import matplotlib.pyplot as plt
import io
import base64

csv_file_path = "systemy_dane_oczyszczone.csv"
df = pd.read_csv(csv_file_path)



def calculate_top_words(title):
    doc = df[df["title"] == title]

    #zwróć pustą listę, jeżeli tytul nie znaleziony
    if doc.empty:
        return []

    #pobranie tekstu z combined_text
    text = doc["combined_text"].values[0]
    words = text.lower().split()

    word_freq = pd.Series(words).value_counts().reset_index()
    word_freq.columns = ['word', 'count']

    top_words = word_freq.head(10)  #czy head ma najczęstsze słowa???????

    #tworzenie wykresu

    chart = (
        alt.Chart(top_words)
        .mark_bar()
        .encode(
            x= alt.X("count:Q", title = "liczba wystąpień"),
            y = alt.Y("word:N", sort ="-x", title = "słowo"),
            tooltip= ["word", "count"]
        )
        .properties(title = "top 10 najczęstszych słów")
    )
    # Konwersja wykresu do HTML
    plot_html = chart.to_html()

    # Retrieve additional information (abstract and author names)
    abstract = doc["abstract"].values[0]
    author_names = doc["author_names"].values[0]

    return top_words.values.tolist(), plot_html, abstract, author_names


