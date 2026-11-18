
import pandas as pd
import numpy as np
import os

# ------------------------------------
# 1. LOAD THE DATASET
# ------------------------------------

file_path = "data/online_retail_II.xlsx"

if not os.path.exists(file_path):
    raise FileNotFoundError(
        f"Dataset not found: {file_path}. "
        "Download Online Retail II from UCI."
    )

df = pd.read_excel(file_path)

print("Original Dataset Shape:", df.shape)

# ------------------------------------
# 2. EXPLORE DATASET
# ------------------------------------

print("\nDataset Information:")
print(df.info())

print("\nMissing Values:")
print(df.isnull().sum())

print("\nDuplicate Records:")
print(df.duplicated().sum())

# ------------------------------------
# 3. REMOVE DUPLICATES
# ------------------------------------

df = df.drop_duplicates()

# ------------------------------------
# 4. HANDLE DATE FORMAT
# ------------------------------------

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

# ------------------------------------
# 5. REMOVE INVALID RECORDS
# ------------------------------------

# Remove records without product codes or dates

df = df.dropna(
    subset=["StockCode", "InvoiceDate"]
)

# Identify cancelled transactions

df["InvoiceNo"] = df["InvoiceNo"].astype(str)

cancelled = df["InvoiceNo"].str.startswith("C")

# Keep valid sales transactions

sales = df[
    (~cancelled) &
    (df["Quantity"] > 0) &
    (df["Price"] > 0)
].copy()

# ------------------------------------
# 6. CREATE REVENUE COLUMN
# ------------------------------------

sales["Revenue"] = (
    sales["Quantity"] * sales["Price"]
)

# ------------------------------------
# 7. SAVE CLEANED DATA
# ------------------------------------

os.makedirs("data/processed", exist_ok=True)

sales.to_csv(
    "data/processed/cleaned_retail_data.csv",
    index=False
)

# ------------------------------------
# 8. DISPLAY FINAL RESULTS
# ------------------------------------

print("\nData Cleaning Completed!")

print("Original Records:", len(df))
print("Cleaned Records:", len(sales))

print(
    "Total Revenue:",
    round(sales["Revenue"].sum(), 2)
)

print(
    "Unique Products:",
    sales["StockCode"].nunique()
)
