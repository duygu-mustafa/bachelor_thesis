import numpy as np
import pandas as pd
from scipy.sparse import csr_matrix
from sklearn.preprocessing import MinMaxScaler

from commit_activity.commit import Commit
from commit_activity.issue import Issue

from commit_activity.constants import MAIN_DATASET_COMMITS, ACTIVITY_RULES


def read_rules():
    rules = pd.read_csv(ACTIVITY_RULES)
    rules['keywords'] = rules['keywords'].apply(lambda x: x.split(','))
    rules_dict = rules.set_index('category')['keywords'].to_dict()

    categories = []
    categories += rules['category'].unique().tolist()
    category_ids = {category: i for i, category in enumerate(categories)}
    category_ids['uncategorized'] = -1

    return rules_dict, category_ids


def process_commits(rules, category_ids):
    commits_df = pd.read_csv(MAIN_DATASET_COMMITS)
    # Initialize a dictionary to hold Issue objects, keyed by issue_id
    issues = {}
    all_commits = []

    # Iterate over each row in the DataFrame to create and add Commit instances to their respective Issue
    for index, row in commits_df.iterrows():
        commit = Commit(row['commit_hash'], row['issue_id'], row['timestamp'], row['commit_message'])
        commit.categorize(rules, category_ids)
        all_commits.append(commit)

        # If the issue already exists, add the commit to it; otherwise, create a new Issue
        if row['issue_id'] in issues:
            issues[row['issue_id']].add_commit(commit)
        else:
            issue = Issue(row['issue_id'])
            issue.add_commit(commit)
            issues[row['issue_id']] = issue

    return issues, all_commits


def define_numerical_context_with_type(issue, category_ids):
    for index, commit in enumerate(issue.commits):
        preceding_distance = -1
        following_distance = -1
        preceding_category_id = category_ids['uncategorized']
        following_category_id = category_ids['uncategorized']

        for preceding_index in range(index - 1, -1, -1):
            if issue.commits[preceding_index].category != 'uncategorized':
                preceding_distance = index - preceding_index
                preceding_category_id = category_ids[issue.commits[preceding_index].category]
                break

        for following_index in range(index + 1, len(issue.commits)):
            if issue.commits[following_index].category != 'uncategorized':
                following_distance = following_index - index
                following_category_id = category_ids[issue.commits[following_index].category]
                break

        commit.set_context(preceding_distance, following_distance, preceding_category_id, following_category_id)


def normalize_context_vectors(commits):
    context_features = np.array([commit.context_vector for commit in commits])
    # Initialize the MinMaxScaler
    scaler = MinMaxScaler()
    # Fit the scaler to the context features and transform them
    normalized_context_features = scaler.fit_transform(context_features)
    # Convert the normalized context features back to a sparse matrix, if needed
    normalized_context_sparse = csr_matrix(normalized_context_features)
    return normalized_context_sparse
