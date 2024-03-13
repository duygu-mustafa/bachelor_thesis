import json
import pandas as pd

# List of issue IDs
with open("closed_issues.json", "r") as file:
    issue_ids = json.load(file)

def extract_number(s):
    return int(s.split("/")[1].split("-")[0])

# Function to check if a branch contains any issue ID
def contains_issue(branch, issue_ids):
    try:
        current_issue_id = branch.split("/")[1].split("-")[0]
        return int(current_issue_id) in issue_ids
    except Exception:
        return False

# Read remote branches from file
remote_branches = pd.read_csv("remote_branches.csv", header=None)
branches_list = remote_branches.iloc[:, 0].tolist()


# Filter branches containing issue IDs
closed_branches = list(set([branch for branch in branches_list if contains_issue(branch, issue_ids)]))
closed_branches = sorted(closed_branches, key=extract_number)


# Save the list of closed branches to a JSON file
with open("closed_branches.json", "w", encoding="utf-8") as file:
    json.dump(closed_branches, file)