class Issue:
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.commits = []

    def add_commit(self, commit):
        self.commits.append(commit)
        self.commits.sort(key=lambda x: x.timestamp)

    def get_commits(self):
        """Return all commits in the issue"""
        return self.commits

    def get_nth_commit(self, n):
        """Return the nth commit in the issue"""
        return self.commits[n]

    def get_issue_id(self):
        """Return the issue ID"""
        return self.issue_id

    def get_issue_length(self):
        """Return the number of commits in the issue"""
        return len(self.commits)

    def start_time(self):
        """Return the timestamp of the first commit"""
        if self.commits:
            return min(commit.timestamp for commit in self.commits)
        return None

    def end_time(self):
        """Return the timestamp of the last commit"""
        if self.commits:
            return max(commit.timestamp for commit in self.commits)
        return None

    def duration(self):
        """Return the duration from the first to the last commit"""
        if self.commits:
            return self.end_time() - self.start_time()
        return None

    def __repr__(self):
        return f"Issue({self.issue_id}, Commits: {len(self.commits)})"
