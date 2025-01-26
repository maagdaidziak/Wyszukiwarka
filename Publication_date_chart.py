import altair as alt
import pandas as pd

# Funkcja do generowania wykresu osi czasu
def generate_timeline_chart(result):
    """
    Tworzy interaktywny wykres osi czasu artykułów na podstawie dat publikacji.

    :param result: Lista wyników, gdzie każda lista zawiera szczegóły artykułu, w tym datę publikacji.
    :return: Wykres Altair w formacie HTML.
    """
    # Konwersja wyników do DataFrame
    df = pd.DataFrame(result, columns=[
        'score', 'relevance', 'impact', 'confidence', 'title', 'publicationDate',
        'citationCount', 'venue', 'fieldsOfStudy', 'popularityCategory', 'source'
    ])

    # Sprawdzanie i przekształcenie kolumny publicationDate na typ datetime
    if 'publicationDate' not in df.columns:
        raise ValueError("Kolumna 'publicationDate' nie istnieje w danych.")

    df['publicationDate'] = pd.to_datetime(df['publicationDate'], errors='coerce')

    # Filtrowanie nieprawidłowych dat
    chart = alt.Chart(df).mark_rule().encode(
        x=alt.X('publicationDate:T', title='Publication date',
                axis=alt.Axis(format='%Y-%m',  # Format: Rok-Miesiąc
                              labelAngle=-45,  # Ukośne etykiety dla lepszej czytelności
                              labelFontSize=12,  # Większa czcionka
                              tickCount='month')),  # Każdy miesiąc jako osobny punkt
        y=alt.value(50),  # Stała wysokość - wszystkie artykuły na jednej linii
        color=alt.Color('venue:N', title="Venue"),  # Kolorowanie według miejsca publikacji
        tooltip=['title', 'publicationDate', 'venue']
    ).properties(
        title="Timeline",
        width=900,
        height=120
    )

    return chart#.to_html()