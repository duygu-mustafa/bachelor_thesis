import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import WordNetLemmatizer
from nltk import download
import re

# Download necessary NLTK data (run once)
# download('punkt')
# download('stopwords')
# download('wordnet')

def preprocess_text(text, use_stemming=True, additional_stopwords=set(), remove_numbers=True):
    """Preprocess text data by tokenizing, lowercasing, removing stopwords, punctuation, and special characters."""

    if "remote" in text:
        bp = 4
    additional_stopwords = {"merge", "branch", "pull", "remote", "origin/dev", "dev", "remote-tracking", "master"}
    # Lowercasing
    text = text.lower()

    if remove_numbers:
        # Remove tokens that are entirely numeric
        text = re.sub(r'\b\d+\b', '', text)

    # Tokenization
    tokens = word_tokenize(text)

    # Removing Punctuation and Special Characters
    tokens = [token.strip(string.punctuation) for token in tokens if token.strip(string.punctuation)]

    # Removing Stopwords
    stop_words = set(stopwords.words('english')).union(additional_stopwords)
    assert "remote" in stop_words
    tokens = [token for token in tokens if token not in stop_words and len(token) > 1]

    if use_stemming:
        # Stemming
        stemmer = PorterStemmer()
        tokens = [stemmer.stem(token) for token in tokens]
    else:
        # Lemmatization
        lemmatizer = WordNetLemmatizer()
        tokens = [lemmatizer.lemmatize(token) for token in tokens]

    return ' '.join(tokens)
