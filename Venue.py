
import pandas as pd
#
# def calculate_venue_distribution(result):
#     # Create a DataFrame from the search results
#     df = pd.DataFrame(result)
#
#     print(df.columns.tolist())
#
#     # Count occurrences of each venue
#     venue_counts = df['venue'].value_counts().reset_index()
#     venue_counts.columns = ['venue', 'count']
#
#     # Create a pie chart using Altair
#     pie_chart = (
#         alt.Chart(venue_counts)
#         .mark_arc()
#         .encode(
#             theta=alt.Theta(field="count", type="quantitative"),
#             color=alt.Color(field="venue", type="nominal"),
#             tooltip=["venue", "count"]
#         )
#         .properties(title="Distribution of Venues")
#     )
#
#     # Convert chart to HTML
#     venue_plot_html = pie_chart.to_html()
#
#     return venue_plot_html

import pandas as pd
import base64
import io
import altair as alt


def calculate_venue_distribution(result):
    df = pd.DataFrame(result)
    """
    Generuje interaktywny wykres kołowy rozkładu gazet (venues) przy użyciu Altair.

    :param df: DataFrame zawierający kolumnę 'venue'.
    :return: HTML string zawierający osadzony wykres (Altair chart).
    
    """
    columns = [
        'similarity_score', 'citation_count', 'impact_factor', 'open_access',
        'title', 'publication_date', 'reference_count', 'venue',
        'fields_of_study', 'popularity_category', 'source'
    ]

    df = pd.DataFrame(result, columns = columns)

    # Sprawdzenie, czy kolumna 'venue' istnieje
    if 'venue' not in df.columns:
        raise ValueError("Kolumna 'venue' nie istnieje w danych.")

    # Grupowanie danych i liczenie liczby wystąpień dla każdej gazety
    venue_counts = df['venue'].value_counts().reset_index()
    venue_counts.columns = ['venue', 'count']

    # Tworzenie wykresu kołowego
    chart = alt.Chart(venue_counts).mark_arc().encode(
        theta=alt.Theta(field="count", type="quantitative"),
        color=alt.Color(field="venue", type="nominal", legend=alt.Legend(title="Venue")),
        tooltip=["venue", "count"]
    ).properties(
        title="Venues distribution"

    )

    # Eksport wykresu do HTML
    venue_plot_html = chart#.to_html()
    return venue_plot_html
