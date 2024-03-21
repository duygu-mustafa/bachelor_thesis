

class Commit:
    def __init__(self, commit_hash, issue_id, timestamp, message):
        self.commit_hash = commit_hash
        self.issue_id = issue_id
        self.timestamp = timestamp
        self.message = message
        self.category = None

    def categorize(self, rules):
        """Categorize the commit based on provided rules"""
        for category, keywords in rules.items():
            if any(keyword in self.message.lower() for keyword in keywords):
                self.category = category
                break
        else:
            self.category = 'Undefined'

    def __repr__(self):
        return f"Commit({self.message}, Issue ID: {self.issue_id}, Timestamp: {self.timestamp})"

