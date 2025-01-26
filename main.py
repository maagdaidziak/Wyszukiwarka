import ast
import urllib

import altair
import nltk
import pandas as pd
from flask import Flask, request, render_template
from nltk import RegexpTokenizer

import Similarity_measure
from Wyszukiwarka import Venue, Charts
from Wyszukiwarka.Charts import calculate_top_words

from Wyszukiwarka.Cleaning import df, clean_and_split_category
from Wyszukiwarka.Publication_date_chart import generate_timeline_chart

# Download NLTK data (if not already downloaded)

nltk.download('punkt_tab')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')

# # Load the CSV file
# data = pd.read_csv('systemy_dane.csv')

def clean_and_split_field_of_study(text):
    fields = ast.literal_eval(text)
    return fields

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    corrections = []
    chart_html = ""
    fields_of_study_raw = df['fieldsOfStudy'].apply(clean_and_split_field_of_study)
    fields_of_study = set([item for sublist in fields_of_study_raw for item in sublist])
    print(fields_of_study)

    pop_cat = clean_and_split_category(df, 'popularity_category')
    print(pop_cat)

    venues = clean_and_split_category(df, 'venue')


    if request.method == 'POST':
        # Pobranie danych z formularza z domyślnymi wartościami
        user_input = request.form.get('user_input', '')  # Domyślna wartość to pusty string
        min_reference_count = request.form.get('min_reference_count', None)
        citation_count_min = request.form.get('citation_count_min', None)
        publication_date_min = request.form.get('publication_date_min', None)
        publication_date_max = request.form.get('publication_date_max', None)
        field_of_study = request.form.get('field_of_study', '')
        is_open_access = request.form.get('isOpenAccess') == 'True'
        popularity_category = request.form.get('popularity_category', '')
        venue_category = request.form.get('venue_category', '')

        print(f'Text received: {user_input}', flush=True)
        print('Calculating. Wait.', flush=True)

        titles_and_abstracts = pd.concat([df['combined_text']]).dropna()
        word_list = []

        for text in titles_and_abstracts:
            tokens = RegexpTokenizer(r'\w+').tokenize(str(text).lower())
            word_list.extend(tokens)

        corrected_query_text, corrections  = Similarity_measure.correct_spelling(user_input, word_list)
        print(f'Result from correct_spelling: {corrected_query_text}')
        if not user_input:
            return render_template('prooba.html', error="Wprowadź zapytanie!", result=[])

        result = Similarity_measure.calculate_measures(corrected_query_text, min_reference_count, citation_count_min, publication_date_min, publication_date_max, field_of_study, is_open_access, popularity_category, venue_category)

        if result:
            print("Result:", result)
            venue_plot = Venue.calculate_venue_distribution(result)
            # Generowanie wykresu
            timeline = generate_timeline_chart(result)
            chart_html = altair.vconcat(venue_plot, timeline).to_html()

    return render_template('prooba.html', result=result, corrections= corrections, fields_of_study = fields_of_study, pop_cat=pop_cat, venues=venues, chart_html=chart_html)



@app.route('/document/<title>')
def document(title):

    top_words, plot_url, abstract, author_names = calculate_top_words(title)


    return render_template('document.html',
                           title=title,
                           top_words=top_words,
                           plot_url=plot_url,
    abstract = abstract ,
    author_names = author_names
    )



if __name__ == '__main__':
    app.run(debug=True, port=5000)


#dodanie do wyników abstract, citation count, reference count, author names, num_authors
#do wyszukiwania isOpenAccess, popularity_category, cited (hight/low), top 5 liczby cytowań, wyszukiwanie po najnowszych latach....

