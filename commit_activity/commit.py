import numpy as np

from commit_activity.processing import preprocess_text
from commit_activity.utils import one_hot_encode


class Commit:
    def __init__(self, commit_hash, issue_id, message="", timestamp=None):
        self.commit_hash = commit_hash
        self.issue_id = issue_id
        self.timestamp = timestamp
        self.message = message
        self.normalized_message = preprocess_text(message)
        if commit_hash == 'start':
            self.category = 'start'
        elif commit_hash == 'end':
            self.category = 'end'
        else:
            self.category = None
        self.context_vector = None
        self.cluster = None
        self.activity = None

    def categorize(self, rules, category_to_index):
        """Categorize the commit based on provided rules"""
        for category, keywords in rules.items():
            if any(keyword in self.message.lower() for keyword in keywords):
                self.category = category
                break
        else:
            self.category = 'uncategorized'
        self.category_id = one_hot_encode(self.category, category_to_index)

    def set_context(self, preceding_category_id, following_category_id):
        """Set context information for the commit"""
        self.context_vector = [
            self.category_id,
            preceding_category_id,
            following_category_id
        ]

    def set_context(self, vector):
        """Set context information for the commit"""
        self.context_vector = vector

    def determine_context(self, preceding_category, following_category, category_to_index):
        current_vector = one_hot_encode(self.category, category_to_index)
        preceding_vector = one_hot_encode(preceding_category, category_to_index)
        following_vector = one_hot_encode(following_category, category_to_index)

        # Concatenate the one-hot vectors to form the context vector
        self.context_vector = np.concatenate([preceding_vector, current_vector, following_vector])

    def __repr__(self):
        return f"{self.category} Commit({self.message}, Issue ID: {self.issue_id}, Timestamp: {self.timestamp})"

