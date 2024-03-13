import pandas as pd


with open('../resources/main_issues.csv', 'r', encoding='utf-8') as file:
    lines = file.readlines()


df = pd.DataFrame(columns=["issue_id", "status", "issue_title", "label", "created_at"])
for line in lines:
    parts = line.split(",")
    issue_title = ",".join(parts[2:-2])
    row = {
        "issue_id": parts[0],
        "status": parts[1],
        "issue_title": f'"{issue_title}"',
        "label": parts[-2],
        "created_at": parts[-1].strip(),
    }
    df = df.append(row, ignore_index=True)

df.to_csv("resources/backup_issues.csv", index=False)
