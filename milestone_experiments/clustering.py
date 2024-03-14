import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import PorterStemmer
import string
import numpy as np
import gensim.downloader
from gensim.models import KeyedVectors
from openai import OpenAI


api_key = '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'

client = OpenAI(
  api_key=api_key,  # this is also the default, it can be omitted
)

# word2vec_model_path = 'path_to_word2vec_model.bin'
# word2vec_model = KeyedVectors.load_word2vec_format(word2vec_model_path, binary=True)


# glove_vectors = gensim.downloader.load(word2vec_model_path)

# Preprocessing function
def preprocess_text(text):
    # Lowercasing
    text = text.lower()

    # Tokenization
    tokens = word_tokenize(text)

    # Removing Punctuation and Special Characters
    tokens = [token.strip(string.punctuation) for token in tokens]

    # Removing Stopwords
    stop_words = set(stopwords.words('english'))
    tokens = [token for token in tokens if token not in stop_words]

    # Stemming
    stemmer = PorterStemmer()
    tokens = [stemmer.stem(token) for token in tokens]

    return ' '.join(tokens)


# def generate_embeddings(title):
#     title_embeddings = []
#     for word in title.split():
#         if word in word2vec_model:
#             title_embeddings.append(word2vec_model[word])
#     if len(title_embeddings) > 0:
#         return np.mean(title_embeddings, axis=0)  # Average embeddings of all words
#     else:
#         return np.zeros(word2vec_model.vector_size)


def get_embedding(text, model="text-embedding-3-small"):
   text = text.replace("\n", " ")
   return client.embeddings.create(input = [text], model=model).data[0].embedding


# Load your data into a pandas DataFrame
# Assuming your data is stored in a CSV file named 'issues.csv'
data = pd.read_csv('../resources/main_dataset/main_issues.csv')
data = data[['Title', 'Created At (UTC)']]
df = data.rename(columns={'Title': 'issue_title', 'Created At (UTC)': 'timestamp'})

# Apply preprocessing
df['processed_title'] = df['issue_title'].apply(preprocess_text)
df.to_csv("../resources/processed_issue_titles.csv", index=False)

# Generate embeddings
# df['ada_embedding'] = df["processed_title"].apply(lambda x: get_embedding(x, model='text-embedding-3-small'))


bp = 5


