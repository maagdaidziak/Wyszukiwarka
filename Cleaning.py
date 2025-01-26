import ast
import os.path
import re

import pandas as pd
import simplemma
from nltk.tokenize import RegexpTokenizer
import json
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.tokenize import word_tokenize

with open('stopwords-iso.json', 'r', encoding='utf-8') as file:
    stopword_dict = json.load(file)

nltk.download('punkt')


file_path = 'systemy_dane.csv'
cleaned_file_path = 'systemy_dane_oczyszczone.csv'

def clean_and_split_field_of_study(text):
    # Usuwanie tylko znaków [ ] " " ' oraz konwersja listy na string
    # text = text.replace('[', '').replace(']', '').replace('"', '').replace("'", "").replace(",", "").strip()
    # text = text.replace("Computer Science", "Computer_Science")
    # fields = re.split(r'\s+', text) #podział po białych znakach
    fields = ast.literal_eval(text)
    return fields

def clean_and_split_category(df, column_name):
    unique_values = set(df[column_name].dropna().tolist())
    return unique_values

def clean_and_save_data(file_path, cleaned_file_path):
    #funkcja oczyszczająca dane i zapisujaca je w pliku csv

    print(f"Plik {cleaned_file_path} nie istnieje. Rozpoczynam oczyszczanie danych...")
    df = pd.read_csv(file_path)

    # Stop wordy dla języka angielskiego
    english_stopwords = stopword_dict.get("en", [])



    def clean_and_tokenize(text):
        tokenizer = RegexpTokenizer(r'\w+')
        tokens = tokenizer.tokenize(str(text).lower())
        tokens = [word for word in tokens if word not in english_stopwords]
        lemmatized_tokens = [simplemma.lemmatize(token, lang="en") for token in tokens]  # Lematizacja  angielskich słów
        return lemmatized_tokens


    # Zastosowanie czyszczenia
    df['cleaned_title'] = df['title'].apply(clean_and_tokenize)
    df['cleaned_abstract'] = df['abstract'].apply(clean_and_tokenize)

    df = df.dropna()


    df['cleaned_title'] = df['cleaned_title'].apply(lambda words: [word + ' ' for word in words])
    df['cleaned_title'] = df['cleaned_title'].apply(lambda words: [word * 2 for word in words])  #zwiększanie wagi dla kolumny "title"
    df['combined_text'] = (df['cleaned_title'].apply(lambda x: ' '.join(x)) + ' ' +
                           df['cleaned_abstract'].apply(lambda x: ' '.join(x)))    # stworzenie jednego ciągu tekstu w kolumnie "combined_tex"

    del df['cleaned_title']
    del df['cleaned_abstract']

    #czyszcenie kolumny fieldsOfStudy
    # df["fieldsOfStudy"] = df["fieldsOfStudy"].apply(clean_and_split_field_of_study)

    #filtrowanie po kolumnie isOpenAccess
    df['isOpenAccess'] = df['isOpenAccess'].astype(bool)

    cols_to_convert = ['referenceCount', 'citationCount', 'month_num', 'num_authors']
    df[cols_to_convert] = df[cols_to_convert].astype(int)

    df['publicationDate'] = pd.to_datetime(df['publicationDate'], errors='coerce')

    # Poprawka daty, gdy miesiąc jest brakujący
    mask = df['publicationDate'].dt.month.isna()
    df.loc[mask, 'publicationDate'] = df.loc[mask, 'publicationDate'].apply(lambda x: pd.to_datetime(str(int(x.year)) + '-01-01'))



    df.to_csv(cleaned_file_path, index=False)

if os.path.exists(cleaned_file_path):
    print(f"Plik {cleaned_file_path} już istnieje. oczyszczanie zostało pominięte.")
    df = pd.read_csv(cleaned_file_path)
else:
    df = clean_and_save_data(file_path, cleaned_file_path)


print("koniec")


#ewentualna zamiana innych typów danych