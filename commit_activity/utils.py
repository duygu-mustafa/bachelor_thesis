import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MinMaxScaler

from commit_activity.constants import ACTIVITY_RULES


def one_hot_encode(category, category_to_index):
    vector_length = len(category_to_index)
    vector = np.zeros(vector_length)
    if category == 'uncategorized':
        return vector
    index = category_to_index[category]
    vector[index] = 1
    return vector


def read_rules():
    rules = pd.read_csv(ACTIVITY_RULES)
    rules['keywords'] = rules['keywords'].apply(lambda x: x.split(','))
    rules_dict = rules.set_index('category')['keywords'].to_dict()

    unique_categories = ['start', 'end']
    unique_categories += rules['category'].unique().tolist()
    category_to_index = {category: index for index, category in enumerate(unique_categories)}

    return rules_dict, category_to_index


def normalize_context_vectors(commits):
    context_features = np.array([commit.context_vector for commit in commits])
    # Initialize the MinMaxScaler
    scaler = MinMaxScaler()
    # Fit the scaler to the context features and transform them
    normalized_context_features = scaler.fit_transform(context_features)
    # Convert the normalized context features back to a sparse matrix, if needed
    normalized_context_sparse = csr_matrix(normalized_context_features)
    return normalized_context_sparse
