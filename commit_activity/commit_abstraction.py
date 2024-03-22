import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix, hstack

from commit_activity.utils import read_rules, process_commits, define_numerical_context_with_type


def abstract_commits():
    # read pre-defined rules
    rules, category_ids = read_rules()

    # group commits in sequences by issue_id and initial categories
    issues, all_commits = process_commits(rules, category_ids)

    # remove one commit issues
    filtered_issues = {issue_id: issue for issue_id, issue in issues.items() if len(issue.commits) > 1}
    filtered_commits = [commit for commit in all_commits if commit.issue_id in filtered_issues]

    # define context for each commit in issues
    for issue in filtered_issues.values():
        define_numerical_context_with_type(issue, category_ids)

    # vectorize commits
    tfidf_vectorizer = TfidfVectorizer()

    commit_messages = [commit.normalized_message for commit in filtered_commits]
    tfidf_matrix = tfidf_vectorizer.fit_transform(commit_messages)

    context_vectors = [commit.context_vector for commit in filtered_commits]
    context_matrix = csr_matrix(np.array(context_vectors))

    combined_features = hstack([tfidf_matrix, context_matrix])

    # perform clustering
    n_clusters = 6  # Adjust based on your analysis

    clustering_model = KMeans(n_clusters=n_clusters, random_state=42)
    cluster_labels = clustering_model.fit_predict(combined_features)

    for commit, label in zip(filtered_commits, cluster_labels):
        commit.cluster = label

    # save the results
    commit_clusters = pd.DataFrame({
        'issue_id': [commit.issue_id for commit in filtered_commits],
        'commit_hash': [commit.commit_hash for commit in filtered_commits],
        'timestamp': [commit.timestamp for commit in filtered_commits],
        'commit_message': [commit.message for commit in filtered_commits],
        'cluster': [commit.cluster for commit in filtered_commits]
    })

    a = 5

if __name__ == '__main__':
    abstract_commits()
