import pandas as pd
import re

def extract_issue_id(commit_message):
    match = re.search(r'#(\d+)', commit_message)
    if match:
        return match.group(1)
    else:
        return None

if __name__ == "__main__":
    path = "resources/backup_commit_history_with_issue_ids.csv"
    with open(path, 'r', encoding='utf-8') as file:
        # Read the first line to get column names
        column_names = file.readline().strip().split(',')
        # Read the rest of the lines
        lines = file.readlines()

    # Split lines and limit splitting to the first three commas
    data = [line.strip().split(',', maxsplit=4) for line in lines]
    df = pd.DataFrame(data, columns=column_names).reset_index(drop=True)

    df['issue_id'] = df['commit_message'].apply(extract_issue_id)
    df["commit_message"] = df["commit_message"].apply(lambda x: f'"{x}"')
    df.to_csv("resources/commit_history_normalized.csv", index=False)

    notnone = df["issue_id"].notna()

    issues_notna = df[notnone]
    issues_notna["issue_id"] = issues_notna["issue_id"].astype(int)
    issues_notna = issues_notna[
        ['issue_id', 'commit_hash', 'commit_message', 'author_name', 'author_email', 'timestamp']]
    issues_notna.to_csv("resources/backup_dataset/backup_commit_history_with_issue_ids.csv", index=False)