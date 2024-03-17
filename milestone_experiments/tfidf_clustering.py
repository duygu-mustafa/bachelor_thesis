import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans

issues_df = pd.read_csv('../resources/processed_issue_titles.csv')
issues = issues_df['processed_title']

vectorizer = TfidfVectorizer(stop_words='english', lowercase=True)

tfidf_matrix = vectorizer.fit_transform(issues)

similarity_matrix = cosine_similarity(tfidf_matrix)

num_clusters = 7  # Specify the number of clusters
kmeans = KMeans(n_clusters=num_clusters)
cluster_labels = kmeans.fit_predict(similarity_matrix)

issues_df['cluster'] = cluster_labels

a = 5
print(issues_df)


