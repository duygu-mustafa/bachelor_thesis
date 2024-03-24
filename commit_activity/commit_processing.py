import numpy as np
import pandas as pd

from commit_activity.commit import Commit
from commit_activity.constants import MAIN_DATASET_COMMITS
from commit_activity.issue import Issue
from commit_activity.utils import one_hot_encode


def process_commits(rules, category_to_index):
    commits_df = pd.read_csv(MAIN_DATASET_COMMITS)
    # Initialize a dictionary to hold Issue objects, keyed by issue_id
    issues = {}
    all_commits = []

    # Iterate over each row in the DataFrame to create and add Commit instances to their respective Issue
    for index, row in commits_df.iterrows():
        commit = Commit(row['commit_hash'], row['issue_id'], row['commit_message'], row['timestamp'])
        commit.categorize(rules, category_to_index)
        all_commits.append(commit)

        # If the issue already exists, add the commit to it; otherwise, create a new Issue
        if row['issue_id'] in issues:
            issues[row['issue_id']].add_commit(commit)
        else:
            issue = Issue(row['issue_id'])
            issue.add_commit(commit)
            issues[row['issue_id']] = issue

    return issues, all_commits


def define_context(issue, category_to_index):
    # Assuming 'uncategorized' has its one-hot representation in category_to_index
    uncategorized_vector = one_hot_encode('uncategorized', category_to_index)

    for index, commit in enumerate(issue.commits):
        # Set the default preceding and following vectors to 'uncategorized'
        preceding_vector = uncategorized_vector
        following_vector = uncategorized_vector

        # preceding commit if it exists and is not 'uncategorized'
        if index > 0 and issue.commits[index - 1].category != 'uncategorized':
            preceding_vector = one_hot_encode(issue.commits[index - 1].category, category_to_index)

        # following commit if it exists and is not 'uncategorized'
        if index < len(issue.commits) - 1 and issue.commits[index + 1].category != 'uncategorized':
            following_vector = one_hot_encode(issue.commits[index + 1].category, category_to_index)

        current_vector = one_hot_encode(commit.category, category_to_index)

        commit.set_context(np.concatenate([preceding_vector, current_vector, following_vector]))
