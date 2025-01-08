import nltk
import pandas as pd
from flask import Flask, request, render_template

import Similarity_measure

# Download NLTK data (if not already downloaded)

# nltk.download('punkt_tab')
# nltk.download('wordnet')
# nltk.download('omw-1.4')
# nltk.download('punkt')
#
# # Load the CSV file
# data = pd.read_csv('systemy_dane.csv')


app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = []
    if request.method == 'POST':
        user_input = request.form['user_input']
        min_reference_count = request.form['min_reference_count']
        citation_count_min = request.form['citation_count_min']
        publication_date_min = request.form['publication_date_min']
        publication_date_max = request.form['publication_date_max']
        print(f'Text received: {user_input}', flush=True)
        print('Calculating. Wait.', flush=True)
        result = Similarity_measure.calculate_measures(user_input, min_reference_count, citation_count_min, publication_date_min, publication_date_max)
        # return f'Result: {result}'
    return render_template('prooba.html', result=result)

if __name__ == '__main__':
    app.run(debug=True, port=5000)


#dodanie do wyników abstract, citation count, reference count, author names, num_authors
#do wyszukiwania isOpenAccess, popularity_category, cited (hight/low), top 5 liczby cytowań, wyszukiwanie po najnowszych latach....

