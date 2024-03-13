import csv

import pandas as pd


if __name__ == '__main__':

    # # Define column names
    # column_names = ['commit_id', 'contributor_name', 'contributor_email', 'commit_message']
    #
    # # Read CSV file
    # with open('first_backup_commit_history.csv', 'r', encoding='utf-8') as file:
    #     lines = file.readlines()
    #
    # # Split lines and limit splitting to the first three commas
    # data = [line.strip().split(',', maxsplit=3) for line in lines]
    #
    # # Convert data to DataFrame and add column names
    # df = pd.DataFrame(data, columns=column_names).reset_index(drop=True)
    #
    # df.to_csv("backup_commit_history.csv", index=False)

    # Read CSV file
    with open('../resources/commit_history.csv', 'r', encoding='utf-8') as file:
        lines = file.readlines()

    # Split lines and limit splitting to the first three commas
    data = [line.strip().split(',', maxsplit=4) for line in lines]

    # Convert data to DataFrame and add column names
    df = pd.DataFrame(data).reset_index(drop=True)

    df.to_csv("backup_issues.csv", index=False)
    print(df)
