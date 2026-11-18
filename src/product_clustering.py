
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import os

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler

# ----------------------------------
# 1. LOAD CLEANED DATA
# ----------------------------------

df = pd.read_csv(
    "data/processed/cleaned_retail_data.csv"
)

print("Dataset loaded successfully!")

# ----------------------------------
# 2. CREATE PRODUCT FEATURES
# ----------------------------------

product_features = df.groupby(
    "StockCode"
).agg(
    total_demand=("Quantity", "sum"),
    average_demand=("Quantity", "mean"),
    demand_variability=("Quantity", "std"),
    total_revenue=("Revenue", "sum"),
    transaction_frequency=("InvoiceNo", "nunique")
).fillna(0)

print("\nProduct Features:")
print(product_features.head())

# ----------------------------------
# 3. PREPARE DATA
# ----------------------------------

# Log transformation reduces
# the effect of extreme values

cluster_data = np.log1p(
    product_features
)

# Standardize features

scaler = StandardScaler()

scaled_data = scaler.fit_transform(
    cluster_data
)

# ----------------------------------
# 4. APPLY K-MEANS CLUSTERING
# ----------------------------------

kmeans = KMeans(
    n_clusters=3,
    random_state=42,
    n_init=10
)

product_features["Cluster"] = (
    kmeans.fit_predict(scaled_data)
)

print("\nClustering completed!")

# ----------------------------------
# 5. IDENTIFY CLUSTER TYPES
# ----------------------------------

cluster_summary = (
    product_features.groupby("Cluster")
    .agg(
        average_demand=("average_demand", "mean"),
        total_demand=("total_demand", "mean"),
        average_revenue=("total_revenue", "mean")
    )
)

# Rank clusters by average demand

cluster_order = (
    cluster_summary["average_demand"]
    .sort_values()
    .index
)

cluster_labels = {
    cluster_order[0]: "Low Demand",
    cluster_order[1]: "Medium Demand",
    cluster_order[2]: "High Demand"
}

product_features["Demand_Category"] = (
    product_features["Cluster"].map(
        cluster_labels
    )
)

print("\nDemand Category Summary:")

print(
    product_features["Demand_Category"]
    .value_counts()
)

# ----------------------------------
# 6. VISUALIZE CLUSTERS
# ----------------------------------

os.makedirs(
    "reports/visualizations",
    exist_ok=True
)

plt.figure(figsize=(10, 6))

sns.scatterplot(
    data=product_features,
    x="total_demand",
    y="total_revenue",
    hue="Demand_Category",
    palette="viridis",
    alpha=0.7
)

plt.title("Product Demand Clustering")
plt.xlabel("Total Product Demand")
plt.ylabel("Total Product Revenue")

plt.tight_layout()

plt.savefig(
    "reports/visualizations/product_clusters.png"
)

plt.show()

# ----------------------------------
# 7. SAVE RESULTS
# ----------------------------------

product_features.to_csv(
    "reports/product_clustering_results.csv"
)

print("\nProduct clustering results saved!")

print("\nProject analysis completed!")

# What does this code do?
# Groups retail transactions by product.

# Calculates total demand and average demand.

# Measures demand variability.

# Calculates product revenue and transaction frequency.

# Applies K-Means clustering.

# Categorizes products into three demand groups.

# Creates a visualization.

# Exports the clustering results to CSV.