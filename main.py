import pandas as pd
import re

def extract_issue_id(commit_message):
    match = re.search(r'#(\d+)', commit_message)
    if match:
        return match.group(1)
    else:
        return None

if __name__ == "__main__":

    issues = pd.read_csv("resources/commit_history_normalized.csv")
    # count issue_ids fields that aren none
    issue_ids = issues["issue_id"].count()
    notnone = issues["issue_id"].notna()

    issues_notna = issues[notnone]
    issues_notna["issue_id"] = issues_notna["issue_id"].astype(int)
    issues_notna = issues_notna[['issue_id','commit_hash', 'commit_message', 'author_name', 'author_email', 'timestamp']]
    issues_notna.to_csv("resources/backup_dataset/backup_commit_history_with_issue_ids.csv", index=False)
    a = 5