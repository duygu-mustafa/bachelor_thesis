import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans
from scipy.sparse import csr_matrix, hstack


from commit_activity.commit import Commit
from commit_activity.issue import Issue

MAIN_DATASET_COMMITS = '../resources/main_dataset/main_commit_history_with_issue_ids.csv'
MAIN_DATASET_ISSUES = '../resources/main_dataset/main_issue_history.csv'
ACTIVITY_RULES = '../resources/activity_rules.csv'
BACKUP_DATASET_COMMITS = '../resources/backup_dataset/backup_commit_history_with_issue_ids.csv'
BACKUP_DATASET_ISSUES = '../resources/backup_dataset/backup_issue_history.csv'


def read_rules():
    rules = pd.read_csv(ACTIVITY_RULES)
    rules['keywords'] = rules['keywords'].apply(lambda x: x.split(','))
    rules_dict = rules.set_index('category')['keywords'].to_dict()

    # categories = ['undefined']
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
