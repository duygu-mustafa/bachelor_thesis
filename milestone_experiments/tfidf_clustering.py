import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

issues_df = pd.read_csv('../resources/processed_issue_titles.csv')

issues = issues_df['processed_title']

vectorizer_title = TfidfVectorizer(stop_words='english', lowercase=True)
tfidf_matrix_title = vectorizer_title.fit_transform(issues)

timestamps = issues_df['timestamp']
timestamps = pd.to_datetime(timestamps)

scaler_timestamp = StandardScaler()
timestamps_scaled = scaler_timestamp.fit_transform(timestamps.values.reshape(-1, 1))

combined_features = pd.concat([pd.DataFrame(tfidf_matrix_title.toarray()), pd.DataFrame(timestamps_scaled)], axis=1)

similarity_matrix = cosine_similarity(combined_features)

num_clusters = 10  # Specify the number of clusters
kmeans = KMeans(n_clusters=num_clusters)
cluster_labels = kmeans.fit_predict(similarity_matrix)

issues_df['cluster'] = cluster_labels

print(issues_df)


