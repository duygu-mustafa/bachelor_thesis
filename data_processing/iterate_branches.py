import json
import os
import subprocess
import pandas as pd

from extract_closed_branches import extract_number


def run_command(command):
    process = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    output, error = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(error.decode("utf-8"))
    else:
        print(output.decode("utf-8"))

def read_csv(path):
    with open(path, 'r', encoding='utf-8') as file:
        # Read the first line to get column names
        column_names = file.readline().strip().split(',')
        # Read the rest of the lines
        lines = file.readlines()

    # Split lines and limit splitting to the first three commas
    data = [line.strip().split(',', maxsplit=4) for line in lines]

    # Convert data to DataFrame and add column names
    return pd.DataFrame(data, columns=column_names).reset_index(drop=True)


global_commit_history = pd.read_csv("global_commit_history.csv")

with open("closed_branches.json", "r") as file:
    branches = json.load(file)

# Define the terminal commands to run
add_columns_to_current_history = ('echo commit_hash,author_name,author_email,timestamp,commit_message > '
                                  'current_commit_history.csv')
download_current_commit_history = ('git log --pretty=format:"%h,%an,%ae,%ad,%s" --date=format:"%Y-%m-%d %H:%M:%S" >> '
                                   'current_commit_history.csv')

for branch in branches:
    subprocess.run(["git", "checkout", branch])
    run_command(add_columns_to_current_history)
    run_command(download_current_commit_history)

    issue_id = extract_number(branch)

    current_commit_history = read_csv("current_commit_history.csv")

    new_commits = current_commit_history[~current_commit_history['commit_hash'].isin(global_commit_history['commit_hash'])]

    new_commits['issue_id'] = issue_id

    global_commit_history = pd.concat([global_commit_history, new_commits], ignore_index=True)

    os.remove("current_commit_history.csv")


global_commit_history.to_csv("global_commit_history.csv", index=False)
