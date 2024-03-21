import pandas as pd


def read_rules():
    rules = pd.read_csv('../resources/activity_rules.csv')
    rules['keywords'] = rules['keywords'].apply(lambda x: x.split(','))
    rules_dict = {}
    for index, row in rules.iterrows():
        for keyword in row['keywords']:
            rules_dict[keyword] = row['category']
    return rules_dict


def abstract_commits():
    # read pre-defined rules
    rules = read_rules()

    # group commits in sequences by issue_id

    # identify initial categories

    # define context for each commit and vectorize

    # train clustering model

    # manually assign categories to clusters


if __name__ == '__main__':
    abstract_commits()
