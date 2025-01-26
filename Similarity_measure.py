from collections import defaultdict, Counter
import math
import re
import pandas as pd
from nltk.tokenize import RegexpTokenizer
import Levenshtein


# import simplemma
# from datetime import datetime
def calculate_tf(document):
    word_counts = Counter(document)
    max_frequency = max(word_counts.values())

    tf_values = {word: count / max_frequency for word, count in word_counts.items()}
    return tf_values


def calculate_idf(documents):
    word_count = defaultdict(int)
    num_documents = len(documents)
    idf_values = {}

    for doc in documents:
        unique_words = set(doc)
        for word in unique_words:
            word_count[word] += 1

    for word, count in word_count.items():
        idf = math.log10(num_documents / count)
        idf_values[word] = idf

    return idf_values


def calculate_tf_idf(documents, idf_values):
    tf_idf_values = []

    for doc in documents:
        tf = calculate_tf(doc)
        tf_idf = {word: tf_value * idf_values[word] for word, tf_value in tf.items()}
        tf_idf_values.append(tf_idf)

    return tf_idf_values


# Function to calculate Levenshtein distance and suggest corrections
def correct_spelling(user_input, word_list):
    words = user_input.split()
    corrected_words = []
    # word_frequency = Counter(word_list)
    single_words = set(word_list)
    corrections = []

    for word in words:
        if word in single_words:
            corrected_words.append(word)
        else:
            # find candidates with Levenstein <2
            candidates = [w for w in single_words if Levenshtein.distance(word, w) <= 2]
            if candidates:
                # Get the most common candidate
                print("candidates and count")
                for i in candidates:
                    print(f"{i}: {word_list.count(i)}")
                best_match = max(candidates, key=lambda w: word_list.count(w))
                corrected_words.append(best_match)
                corrections.append((word, best_match))  #dodane do correctins = []
            else:
                corrected_words.append(word)

    corrected_text = ' '.join(corrected_words)
    return corrected_text, corrections

def calculate_measures(query_text, min_reference_count, citation_count_min, publication_date_min, publication_date_max, field_of_study, is_open_access, popularity_category, venue_category):
    df = pd.read_csv('systemy_dane_oczyszczone.csv')

    # Load words from titles and abstracts for spelling correction
    word_list = []
    for text in df['combined_text'].dropna():
        tokens = RegexpTokenizer(r'\w+').tokenize(str(text).lower())
        word_list.extend(tokens)

    # Correct spelling in user input
    corrected_query_text = correct_spelling(query_text, word_list)

    if min_reference_count != "":
        df = df[df['referenceCount'] >= int(min_reference_count)]
    if citation_count_min != "":
        df = df[df['citationCount'] <= int(citation_count_min)]
    if publication_date_min != "":
        df = df[df['publicationDate'] >= publication_date_min]
    if publication_date_max != "":
        df = df[df['publicationDate'] <= publication_date_max]
    if field_of_study != "":
        df = df[df['fieldsOfStudy'].str.contains(field_of_study, case=False, na=False)]
    if is_open_access != "":
        if isinstance(is_open_access, bool):
            df = df[df['isOpenAccess'] == is_open_access]
    if popularity_category != "":
        df = df[df['popularity_category'].str.contains(popularity_category, case=False, na=False)]
    if venue_category != "":
        df = df[df['venue'].str.contains(venue_category, case=False, na=False)]


    # Tokenizacja dokumentów
    tokenizer = RegexpTokenizer(r'\w+')
    documents = df['combined_text'].apply(lambda x: tokenizer.tokenize(str(x).lower())).tolist()
    idf_values = calculate_idf(documents)
    tf_idf_values = calculate_tf_idf(documents, idf_values)

    # TF-IDF dla zapytania
    query_tf = tokenizer.tokenize(str(corrected_query_text).lower())
    query_tf_idf = {word: query_tf.count(word) / len(query_tf) * idf_values.get(word, 0) for word in
                    query_tf}

    #obliczanie miar podobieństwa
    results = []
    for index, doc_tf_idf in enumerate(tf_idf_values):
        result = []
        sum_squared_tf_idf = sum(value ** 2 for word, value in doc_tf_idf.items() if word in query_tf)

        if sum_squared_tf_idf != 0:
            iloczyn = sum(doc_tf_idf.get(word, 0) for word in query_tf if word in doc_tf_idf)
            result.append(round(iloczyn, 3))
            dice = (2 * iloczyn) / (4 * sum_squared_tf_idf)
            result.append(round(dice, 3))
            jaccard = iloczyn / (4 + sum_squared_tf_idf - iloczyn)
            result.append(round(jaccard, 3))
            cosinus = iloczyn / (math.sqrt(4) * math.sqrt(sum_squared_tf_idf))
            result.append(round(cosinus, 3))
            result.append(index)
            results.append(result)

    sorted_articles = sorted(results, key=lambda x: (x[3], x[2], x[1], x[0]), reverse=True)

    top_3_articles = sorted_articles[:5]
    for article in top_3_articles:
        id_of_article = article[4]
        article.pop(4)
        article_info = df.iloc[id_of_article]
        article.append(article_info['title'])
        # article.append(article_info['abstract'])
        article.append(article_info['publicationDate'])
        article.append(article_info['referenceCount'])
        article.append(article_info['venue'])
        article.append(article_info['fieldsOfStudy'])
        article.append(article_info['popularity_category'])
        article.append(article_info['venue'])
        # article.pop(4)

    print(top_3_articles)

    return top_3_articles