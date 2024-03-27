import numpy as np
import spacy
from scipy.spatial.distance import cosine
from scipy.optimize import linear_sum_assignment

from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


from commit_activity.commit_processing import process_commits


def topic_modeling_keywords(n_components=8):
    """Perform topic modeling on commit messages and return the top keywords for each topic."""
    issues, all_commits = process_commits(None, None, categorize=False)
    filtered_issues = {issue_id: issue for issue_id, issue in issues.items() if len(issue) > 3}
    filtered_commits = [commit for commit in all_commits if commit.issue_id in filtered_issues]
    commit_messages = [commit.normalized_message for commit in filtered_commits]

    # Vectorize commit messages
    vectorizer = CountVectorizer(max_df=0.95, min_df=2, stop_words='english')
    dtm = vectorizer.fit_transform(commit_messages)

    # Apply LDA
    lda = LatentDirichletAllocation(n_components=8, random_state=13)  # n_components is the number of topics
    lda.fit(dtm)

    # Display top words for each topic
    feature_names = vectorizer.get_feature_names_out()
    topics_with_keywords = {}
    for topic_idx, topic in enumerate(lda.components_):
        topics_with_keywords[topic_idx] = [feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]
        print(f"Topic #{topic_idx}:")
        print(" ".join([feature_names[i] for i in topic.argsort()[:-10 - 1:-1]]))

    return list(topics_with_keywords.values())


def calculate_average_vector(words):
    """Calculate the average vector of a list of words using their embeddings."""
    vectors = [nlp(word).vector for word in words]
    average_vector = sum(vectors) / len(words)
    return average_vector


def assign_activities_to_topics(activities, topic_keywords):
    """Find the closest activity for each topic based on keyword embeddings."""
    # Construct the cost matrix
    cost_matrix = np.zeros((len(activities), len(topic_keywords)))

    for i, activity in enumerate(activities):
        activity_vector = nlp(activity).vector
        for j, keywords in enumerate(topic_keywords):
            topic_vector = calculate_average_vector(keywords)
            # Inverting similarity to represent cost; Adjust as needed based on your similarity measure
            cost_matrix[i, j] = 1 - (1 - cosine(activity_vector, topic_vector))

    # Find the optimal assignment
    row_ind, col_ind = linear_sum_assignment(cost_matrix)

    # Map the activities to keyword lists based on the optimal assignment
    activity_to_keywords_mapping = {activities[i]: topic_keywords[j] for i, j in zip(row_ind, col_ind)}
    return activity_to_keywords_mapping


if __name__ == '__main__':
    activities = ["feature","bugfix","refactoring","documentation","test","configuration", "meeting",]
    nlp = spacy.load('en_core_web_lg')

    topic_keywords = topic_modeling_keywords(len(activities))
    activities_with_keywords = assign_activities_to_topics(activities, topic_keywords)
    a = 1

