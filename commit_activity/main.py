import pandas as pd

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
    return rules_dict

def process_commits(rules):
    commits_df = pd.read_csv(MAIN_DATASET_COMMITS)
    # Initialize a dictionary to hold Issue objects, keyed by issue_id
    issues = {}

    # Iterate over each row in the DataFrame to create and add Commit instances to their respective Issue
    for index, row in commits_df.iterrows():
        commit = Commit(row['commit_hash'], row['issue_id'], row['timestamp'], row['commit_message'])
        commit.categorize(rules)

        # If the issue already exists, add the commit to it; otherwise, create a new Issue
        if row['issue_id'] in issues:
            issues[row['issue_id']].add_commit(commit)
        else:
            issue = Issue(row['issue_id'])
            issue.add_commit(commit)
            issues[row['issue_id']] = issue

    return issues


def abstract_commits():
    # read pre-defined rules
    rules = read_rules()

    # group commits in sequences by issue_id
    issues = process_commits(rules)

    # identify initial categories

    # define context for each commit and vectorize

    # train clustering model

    # manually assign categories to clusters


if __name__ == '__main__':
    abstract_commits()
