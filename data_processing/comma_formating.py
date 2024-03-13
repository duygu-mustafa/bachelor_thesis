import pandas as pd
def read_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        # Read the first line to get column names
        column_names = file.readline().strip().split(',')
        # Read the rest of the lines
        lines = file.readlines()

    # Split lines and limit splitting to the first three commas
    data = [line.strip().split(',', maxsplit=5) for line in lines]

    # Convert data to DataFrame and add column names
    return pd.DataFrame(data, columns=column_names).reset_index(drop=True)

df = read_csv("../resources/global_commit_history_with_issue_id.csv")
df["commit_message"] = df["commit_message"].apply(lambda x: f'"{x}"')
df.to_csv("main_commit_history_with_issue_ids.csv", index=False)
a=6