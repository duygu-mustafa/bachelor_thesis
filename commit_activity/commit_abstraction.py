import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans, AgglomerativeClustering, DBSCAN
from scipy.sparse import issparse

from commit_activity.plot_clusters import visualize_clusters_with_tsne
from commit_activity.sequence_mining import mine_frequent_patterns, apply_freq_pattern_mapping
from commit_activity.utils import (
    read_rules,
    process_commits,
    define_numerical_context_with_type,
    normalize_context_vectors,
)


def apply_clustering(features, algorithm='kmeans', n_clusters=5, **kwargs):
    if issparse(features) and algorithm != 'kmeans':
        print(f"Converting features to dense format for {algorithm} algorithm...")
        features = features.toarray()

    # Choose and apply the clustering algorithm
    print(f"Applying {algorithm} clustering...")
    if algorithm == 'kmeans':
        model = KMeans(n_clusters=n_clusters, **kwargs)
    elif algorithm == 'agglomerative':
        model = AgglomerativeClustering(n_clusters=n_clusters, **kwargs)
    elif algorithm == 'dbscan':
        model = DBSCAN(**kwargs)
    else:
        raise ValueError("Unsupported clustering algorithm.")

    cluster_labels = model.fit_predict(features)

    return cluster_labels


def abstract_commits():
    # read pre-defined rules
    rules, category_ids = read_rules()

    # group commits in sequences by issue_id and initial categories
    issues, all_commits = process_commits(rules, category_ids)

    # remove one commit issues
    filtered_issues = {issue_id: issue for issue_id, issue in issues.items() if len(issue.commits) > 1}
    filtered_commits = [commit for commit in all_commits if commit.issue_id in filtered_issues]

    # mine frequent patterns and apply to commits
    mapping = mine_frequent_patterns(filtered_issues)
    apply_freq_pattern_mapping(filtered_issues, mapping, category_ids)

    # define context for each commit in issues
    for issue in filtered_issues.values():
        define_numerical_context_with_type(issue, category_ids)

    # vectorize commits
    tfidf_vectorizer = TfidfVectorizer()

    commit_messages = [commit.normalized_message for commit in filtered_commits]
    tfidf_matrix = tfidf_vectorizer.fit_transform(commit_messages)

    # case1: context not minmax scaled
    # context_vectors = [commit.context_vector for commit in filtered_commits]
    # context_matrix = csr_matrix(np.array(context_vectors))

    context_matrix = normalize_context_vectors(filtered_commits)

    # combined_features = hstack([tfidf_matrix, context_matrix])
    combined_features = tfidf_matrix # Use this line if you only want to use TF-IDF features
    # perform clustering
    n_clusters = 6  # Adjust based on your analysis

    cluster_labels = apply_clustering(
        features=combined_features,
        n_clusters=n_clusters,
        algorithm='kmeans',
        # eps=0.5,  # Example parameter for DBSCAN
        # min_samples=5
    )

    for commit, label in zip(filtered_commits, cluster_labels):
        commit.cluster = label

    # visualize the clusters
    visualize_clusters_with_tsne(combined_features, cluster_labels)

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
