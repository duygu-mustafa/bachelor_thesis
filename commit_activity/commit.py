from commit_activity.processing import preprocess_text


class Commit:
    def __init__(self, commit_hash, issue_id, timestamp, message):
        self.commit_hash = commit_hash
        self.issue_id = issue_id
        self.timestamp = timestamp
        self.message = message
        self.normalized_message = preprocess_text(message)
        self.category = None
        self.category_id = -1
        self.context = {
            'preceding_distance': -1,
            'following_distance': -1,
            'preceding_category_id': None,
            'following_category_id': None
        }
        self.context_vector = None
        self.cluster = None

    def categorize(self, rules, category_ids):
        """Categorize the commit based on provided rules"""
        for category, keywords in rules.items():
            if any(keyword in self.message.lower() for keyword in keywords):
                self.category = category
                break
        else:
            self.category = 'uncategorized'
        self.category_id = category_ids.get(self.category, -1)

    def set_context(self, preceding_distance, following_distance, preceding_category_id, following_category_id):
        """Set context information for the commit"""
        self.context['preceding_distance'] = preceding_distance
        self.context['following_distance'] = following_distance
        self.context['preceding_category_id'] = preceding_category_id
        self.context['following_category_id'] = following_category_id
        self.context_vector = [
            self.category_id,
            preceding_distance,
            following_distance,
            preceding_category_id,
            following_category_id
        ]

    def __repr__(self):
        return f"{self.category} Commit({self.message}, Issue ID: {self.issue_id}, Timestamp: {self.timestamp})"

