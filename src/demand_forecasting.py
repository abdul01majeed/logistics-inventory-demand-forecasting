
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error
)

import os

# ----------------------------------
# 1. LOAD CLEANED DATA
# ----------------------------------

df = pd.read_csv(
    "data/processed/cleaned_retail_data.csv"
)

df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"]
)

print("Dataset loaded successfully!")

# ----------------------------------
# 2. SELECT TOP PRODUCT
# ----------------------------------

product_sales = (
    df.groupby("StockCode")["Quantity"]
    .sum()
    .sort_values(ascending=False)
)

top_product = product_sales.index[0]

print("Selected Product:", top_product)

product_data = df[
    df["StockCode"] == top_product
].copy()

# ----------------------------------
# 3. CREATE DAILY DEMAND
# ----------------------------------

daily_demand = (
    product_data.groupby(
        product_data["InvoiceDate"].dt.floor("D")
    )["Quantity"]
    .sum()
)

daily_demand = daily_demand.asfreq(
    "D", fill_value=0
)

forecast_data = pd.DataFrame({
    "demand": daily_demand
})

# ----------------------------------
# 4. FEATURE ENGINEERING
# ----------------------------------

forecast_data["lag_1"] = (
    forecast_data["demand"].shift(1)
)

forecast_data["lag_7"] = (
    forecast_data["demand"].shift(7)
)

forecast_data["lag_14"] = (
    forecast_data["demand"].shift(14)
)

forecast_data["rolling_mean_7"] = (
    forecast_data["demand"]
    .shift(1)
    .rolling(7)
    .mean()
)

forecast_data["day_of_week"] = (
    forecast_data.index.dayofweek
)

forecast_data["month"] = (
    forecast_data.index.month
)

forecast_data = forecast_data.dropna()

# ----------------------------------
# 5. SPLIT DATA CHRONOLOGICALLY
# ----------------------------------

features = [
    "lag_1",
    "lag_7",
    "lag_14",
    "rolling_mean_7",
    "day_of_week",
    "month"
]

X = forecast_data[features]

y = forecast_data["demand"]

split = int(len(forecast_data) * 0.8)

X_train = X.iloc[:split]
X_test = X.iloc[split:]

y_train = y.iloc[:split]
y_test = y.iloc[split:]

# ----------------------------------
# 6. TRAIN MODEL
# ----------------------------------

model = RandomForestRegressor(
    n_estimators=100,
    random_state=42,
    max_depth=10
)

model.fit(X_train, y_train)

print("Model training completed!")

# ----------------------------------
# 7. PREDICT DEMAND
# ----------------------------------

predictions = model.predict(X_test)

# ----------------------------------
# 8. MODEL EVALUATION
# ----------------------------------

mae = mean_absolute_error(
    y_test, predictions
)

rmse = np.sqrt(
    mean_squared_error(y_test, predictions)
)

total_actual = y_test.sum()

wape = (
    np.abs(y_test - predictions).sum()
    / total_actual * 100
    if total_actual != 0 else np.nan
)

print("\nMODEL PERFORMANCE")

print("MAE:", round(mae, 2))
print("RMSE:", round(rmse, 2))
print("WAPE (%):", round(wape, 2))

# ----------------------------------
# 9. VISUALIZE RESULTS
# ----------------------------------

os.makedirs(
    "reports/visualizations",
    exist_ok=True
)

plt.figure(figsize=(12, 6))

plt.plot(
    y_test.index,
    y_test,
    label="Actual Demand",
    color="blue"
)

plt.plot(
    y_test.index,
    predictions,
    label="Predicted Demand",
    color="red"
)

plt.title("Actual vs Predicted Product Demand")

plt.xlabel("Date")
plt.ylabel("Demand Quantity")

plt.legend()
plt.tight_layout()

plt.savefig(
    "reports/visualizations/demand_forecast.png"
)

plt.show()

# ----------------------------------
# 10. SAVE FORECAST RESULTS
# ----------------------------------

results = pd.DataFrame({
    "Date": y_test.index,
    "Actual_Demand": y_test.values,
    "Predicted_Demand": predictions
})

results.to_csv(
    "reports/forecast_results.csv",
    index=False
)

print("\nForecast results saved successfully!")

# What will this code accomplish?
# Selects the highest-selling product.

# Calculates daily product demand.

# Creates historical demand features.

# Trains a Random Forest Regression model.

# Predicts future demand for the test period.

# Evaluates the model using MAE, RMSE, and WAPE.

# Generates an actual-versus-predicted demand chart.

# Saves forecasting results as a CSV file.