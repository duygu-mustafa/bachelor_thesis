import pandas as pd

import json

# Your list
my_list = ["item1", "item2", "item3"]

# Save the list to a file


df = pd.read_csv("../resources/main_dataset/main_issues.csv")
issue_ids = list(set(df["Issue ID"].to_list()))

with open("../resources/closed_issues.json", "w") as file:
    json.dump(issue_ids, file)



a = 5