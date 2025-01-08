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
#nltk.download('stopwords')
#print(stopwords.fileids())

file_path = 'systemy_dane.csv'
#### df2 = pd.read_csv('unique_rows_file2.csv')
df = pd.read_csv(file_path)

# Stop wordy dla języka angielskiego
english_stopwords = stopword_dict.get("eng", [])



def clean_and_tokenize(text):
    tokenizer = RegexpTokenizer(r'\w+')
    tokens = tokenizer.tokenize(str(text).lower())
    tokens = [word for word in tokens if word not in english_stopwords]
    lemmatized_tokens = [simplemma.lemmatize(token, lang="en") for token in tokens]  # Lematizacja  angielskich słów
    return lemmatized_tokens


# Zastosowanie czyszczenia
df['cleaned_title'] = df['title'].apply(clean_and_tokenize)
df['cleaned_abstract'] = df['abstract'].apply(clean_and_tokenize)


print("Cleaned and tokenized 'article_title' column:")
print(df['cleaned_title'])

print("\nCleaned and tokenized 'abstract' column:")
print(df['cleaned_abstract'])
df = df.dropna()


df['cleaned_title'] = df['cleaned_title'].apply(lambda words: [word + ' ' for word in words])
df['cleaned_title'] = df['cleaned_title'].apply(lambda words: [word * 2 for word in words])  #zwiększanie wagi dla kolumny "title"
df['combined_text'] = (df['cleaned_title'].apply(lambda x: ' '.join(x)) + ' ' +
                       df['cleaned_abstract'].apply(lambda x: ' '.join(x)))    # stworzenie jednego ciągu tekstu w kolumnie "combined_tex"

del df['cleaned_title']
del df['cleaned_abstract']



cols_to_convert = ['referenceCount', 'citationCount', 'month_num', 'num_authors']
df[cols_to_convert] = df[cols_to_convert].astype(int)

df['publicationDate'] = pd.to_datetime(df['publicationDate'], errors='coerce')

# Poprawka daty, gdy miesiąc jest brakujący
mask = df['publicationDate'].dt.month.isna()
df.loc[mask, 'publicationDate'] = df.loc[mask, 'publicationDate'].apply(lambda x: pd.to_datetime(str(int(x.year)) + '-01-01'))


output_file_path = 'systemy_dane_oczyszczone.csv'
df.to_csv(output_file_path, index=False)
print("koniec")


#ewentualna zamiana innych typów danych