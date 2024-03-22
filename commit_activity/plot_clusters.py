from scipy.sparse import csr_matrix, issparse
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import matplotlib.pyplot as plt
import numpy as np


def visualize_clusters_with_tsne(combined_features, cluster_labels):
    """
    Visualizes clusters of combined commit features using t-SNE.

    Parameters:
    - combined_features: Sparse matrix. The combined TF-IDF and context features for each commit.
    - cluster_labels: Array-like. The cluster labels for each commit.
    """

    # Reduce dimensions with t-SNE
    tsne_model = TSNE(n_components=2, random_state=42)
    # If combined_features is sparse, converting to dense array might be necessary
    reduced_features = tsne_model.fit_transform(combined_features.toarray())

    # Plot the clusters
    plt.figure(figsize=(10, 8))

    # Assign colors to each cluster
    unique_labels = set(cluster_labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        # Filter data points that belong to the current cluster
        class_member_mask = (cluster_labels == k)

        # Plot the data points that are clustered
        xy = reduced_features[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=8, label=f"Cluster {k}")

    plt.title('Clusters visualization with t-SNE')
    plt.xlabel('t-SNE feature 1')
    plt.ylabel('t-SNE feature 2')
    plt.legend()
    plt.show()


def visualize_clusters_with_pca(features, cluster_labels):
    """
    Visualizes clusters using PCA to reduce to 2 dimensions.

    Parameters:
    - features: The original high-dimensional feature set.
    - cluster_labels: Cluster labels for each data point.
    """
    pca = PCA(n_components=2)
    reduced_features = pca.fit_transform(features.toarray() if issparse(features) else features)

    plt.figure(figsize=(10, 8))
    unique_labels = set(cluster_labels)
    colors = plt.cm.rainbow(np.linspace(0, 1, len(unique_labels)))

    for k, col in zip(unique_labels, colors):
        class_member_mask = (cluster_labels == k)
        xy = reduced_features[class_member_mask]
        plt.plot(xy[:, 0], xy[:, 1], 'o', markerfacecolor=col, markeredgecolor='k', markersize=8, label=f"Cluster {k}")

    plt.title('Cluster visualization with PCA')
    plt.legend()
    plt.xlabel('PCA Feature 1')
    plt.ylabel('PCA Feature 2')
    plt.show()

