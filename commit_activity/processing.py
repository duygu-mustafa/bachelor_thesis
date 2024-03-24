import string
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

def preprocess_text(text: ""):
    # Lowercasing
    text = text.lower()
    text = text.replace('merge branch', '')  # Removing common commit message prefix

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