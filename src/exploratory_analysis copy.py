
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# ----------------------------------
# 1. LOAD CLEANED DATA
# ----------------------------------

file_path = "data/processed/cleaned_retail_data.csv"

df = pd.read_csv(file_path)

df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])

print("Dataset loaded successfully!")
print("Dataset Shape:", df.shape)

# ----------------------------------
# 2. CREATE OUTPUT DIRECTORY
# ----------------------------------

os.makedirs("reports/visualizations", exist_ok=True)

sns.set_theme(style="whitegrid")

# ----------------------------------
# 3. TOP 10 BEST-SELLING PRODUCTS
# ----------------------------------

top_products = (
    df.groupby("StockCode")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

top_products.plot(
    kind="bar",
    color="steelblue"
)

plt.title("Top 10 Best-Selling Products")
plt.xlabel("Product Code")
plt.ylabel("Total Quantity Sold")
plt.xticks(rotation=45)

plt.tight_layout()

plt.savefig(
    "reports/visualizations/top_products.png"
)

plt.show()

# ----------------------------------
# 4. MONTHLY SALES ANALYSIS
# ----------------------------------

df["Revenue"] = (
    df["Quantity"] * df["Price"]
)

monthly_sales = (
    df.set_index("InvoiceDate")
    .resample("MS")["Revenue"]
    .sum()
)

plt.figure(figsize=(12, 6))

monthly_sales.plot(
    color="green",
    linewidth=2
)

plt.title("Monthly Retail Revenue")
plt.xlabel("Month")
plt.ylabel("Revenue")

plt.tight_layout()

plt.savefig(
    "reports/visualizations/monthly_sales.png"
)

plt.show()

# ----------------------------------
# 5. DAILY DEMAND ANALYSIS
# ----------------------------------

daily_demand = (
    df.groupby(
        df["InvoiceDate"].dt.date
    )["Quantity"]
    .sum()
)

plt.figure(figsize=(12, 6))

daily_demand.plot(color="orange")

plt.title("Daily Product Demand")
plt.xlabel("Date")
plt.ylabel("Quantity Sold")

plt.tight_layout()

plt.savefig(
    "reports/visualizations/daily_demand.png"
)

plt.show()

# ----------------------------------
# 6. PRODUCT REVENUE ANALYSIS
# ----------------------------------

top_revenue = (
    df.groupby("StockCode")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

plt.figure(figsize=(12, 6))

top_revenue.plot(
    kind="bar",
    color="purple"
)

plt.title("Top 10 Products by Revenue")
plt.xlabel("Product Code")
plt.ylabel("Total Revenue")

plt.tight_layout()

plt.savefig(
    "reports/visualizations/top_revenue.png"
)

plt.show()

# ----------------------------------
# 7. CORRELATION ANALYSIS
# ----------------------------------

numeric_data = df[
    ["Quantity", "Price", "Revenue"]
]

plt.figure(figsize=(8, 5))

sns.heatmap(
    numeric_data.corr(),
    annot=True,
    cmap="coolwarm"
)

plt.title("Sales Data Correlation Heatmap")

plt.tight_layout()

plt.savefig(
    "reports/visualizations/correlation_heatmap.png"
)

plt.show()

# ----------------------------------
# 8. SUMMARY
# ----------------------------------

print("\nEXPLORATORY DATA ANALYSIS COMPLETE")

print("\nTotal Revenue:")
print(round(df["Revenue"].sum(), 2))

print("\nTotal Quantity Sold:")
print(df["Quantity"].sum())

print("\nNumber of Unique Products:")
print(df["StockCode"].nunique())

print("\nVisualizations saved successfully!")

# What this script does
# It generates five visualizations:

# IMLV Final Project
 
# 1. Top 10 Best-Selling Products

# Identifies products with the highest sales quantities.

# How to Make a Line Chart with AI: The Complete 2026 Guide to Design Rules | by Steven Cen | Mar, 2026 | Medium
 
# 2. Monthly Sales Analysis

# Identifies monthly revenue trends.

# Dependence on gas leads the Italian electricity market prices to be among the highest in europe in the first half of 2021 - AleaSoft Energy Forecasting
 
# 3. Daily Demand Analysis

# Shows how product demand changes over time.

# Day 32 — Data Visualization Day 3: Line & Bar Charts in Matplotlib | by Ratnesh | Medium
 
# 4. Product Revenue Analysis

# Identifies products generating the most revenue.

# Exploratory Data Analysis on Iris Dataset – Data Brains
 
# 5. Correlation Heatmap

# Examines relationships between quantity, price, and revenue.