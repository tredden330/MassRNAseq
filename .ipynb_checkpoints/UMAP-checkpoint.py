import cuml
import cudf
import numpy as np
import umap                 #NOTE: To use cuML, an older version of python is needed (3.9) remember to load it!

# Create a synthetic dataset
n_samples = 1000
n_features = 10
random_state = 42

np.random.seed(random_state)
data = np.random.rand(n_samples, n_features)

# Convert the NumPy array to a cuDF DataFrame
gdf_data = cudf.DataFrame(data)

# Initialize the UMAP model
umap_model = cuml.UMAP(n_neighbors=15, n_components=2, random_state=random_state)

# Fit UMAP to the data
umap_embedding = umap_model.fit_transform(gdf_data)

# The resulting umap_embedding is a NumPy array with the lower-dimensional representation

# You can now visualize the UMAP embedding using a plotting library like Matplotlib
import matplotlib.pyplot as plt

plt.scatter(umap_embedding[:, 0], umap_embedding[:, 1])
plt.title("UMAP Projection")
plt.xlabel("UMAP Dimension 1")
plt.ylabel("UMAP Dimension 2")
plt.savefig("/graphs/sample.png")
