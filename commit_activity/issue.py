from commit_activity.commit import Commit


class Issue:
    def __init__(self, issue_id):
        self.issue_id = issue_id
        self.commits = []
        self.commits.append(Commit("start", "StartOfSequence"))
        self.commits.append(Commit("end", "EndOfSequence"))

    def _sort_commits(self):
        start_marker = self.commits.pop(0)  # Remove and keep the start marker
        end_marker = self.commits.pop()  # Remove and keep the end marker

        self.commits.sort(key=lambda x: x.timestamp)

        self.commits.insert(0, start_marker)
        self.commits.append(end_marker)

    def add_commit(self, commit):
        self.commits.insert(-1, commit)
        self._sort_commits()

    def get_commits(self):
        """Return all commits in the issue"""
        return self.commits

    def get_nth_commit(self, n):
        """Return the nth commit in the issue"""
        return self.commits[n-1]

    def get_issue_id(self):
        """Return the issue ID"""
        return self.issue_id

    def start_time(self):
        """Return the timestamp of the first commit"""
        if self.commits:
            commits_without_start_and_end = self.commits[1:-1]
            return min(commit.timestamp for commit in commits_without_start_and_end)
        return None

    def end_time(self):
        """Return the timestamp of the last commit"""
        if self.commits:
            commits_without_start_and_end = self.commits[1:-1]
            return max(commit.timestamp for commit in commits_without_start_and_end)
        return None

    def duration(self):
        """Return the duration from the first to the last commit"""
        if self.commits:
            return self.end_time() - self.start_time()
        return None

    def __iter__(self):
        return iter(self.commits)

    def __len__(self):
        return len(self.commits)

    def __getitem__(self, item):
        return self.commits[item]

    def __repr__(self):
        return f"Issue({self.issue_id}, Commits: {len(self.commits)})"
