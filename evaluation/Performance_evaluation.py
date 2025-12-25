import pandas as pd
import joblib
import matplotlib.pyplot as plt
from sklearn.metrics import mean_absolute_error, mean_squared_error,r2_score
import numpy as np

# Load SARIMA model
model = joblib.load('models/sarima_alcohol_model.pkl')

# Load the test dataset (no hardcoding - reads from CSV)
test_df = pd.read_csv('datasets/test_dataset_2021_2024.csv', parse_dates=['DATUM'], index_col='DATUM')

# Ensuring test_df is sorted by date
test_df = test_df.sort_index()

print("Test data loaded:")
print(f"Test period: {test_df.index.min()} to {test_df.index.max()} ({len(test_df)} months)")

# Number of steps to forecast
steps = len(test_df)

# Generate forecasts using the loaded model
forecast = model.get_forecast(steps=steps)
predictions = forecast.predicted_mean.round()  # Round to nearest integer (accidents are counts)
conf_int = forecast.conf_int()

#  predictions and confidence intervals 
predictions.index = test_df.index
conf_int.index = test_df.index

predictions_rounded = predictions.round()

# results DataFrame
results = pd.DataFrame({
    'Actual': test_df['Value'],
    'Predicted': predictions.astype(int),
    'Lower_95_CI': conf_int['lower Value'].round().astype(int),
    'Upper_95_CI': conf_int['upper Value'].round().astype(int),
    'Absolute_Error': (test_df['Value'] - predictions).abs()
})

#evaluation metrics
mae = mean_absolute_error(test_df['Value'], predictions)
mse = mean_squared_error(test_df['Value'], predictions)
rmse = np.sqrt(mse)
r2 = r2_score(test_df['Value'], predictions)
mape = np.mean(np.abs((test_df['Value'] - predictions) / test_df['Value'])) * 100

print("\n" + "="*60)
print("SARIMA MODEL PERFORMANCE EVALUATION (2021–2024 Test Set)")
print("="*60)
print(f"Mean Absolute Error (MAE)      : {mae:.2f}")
print(f"Mean Squared Error (MSE)       : {mse:.2f}")
print(f"Root Mean Squared Error (RMSE) : {rmse:.2f}")
print(f"R² Score                       : {r2:.3f}")
print(f"Mean Absolute Percentage Error (MAPE): {mape:.2f}%")
print("="*60)

# Print first 12 months for quick view
print("\nFirst 12 Months Comparison:")
print(results.head(12))


# Actual vs Predicted Line Plot
plt.figure(figsize=(14, 7))
plt.plot(test_df.index, test_df['Value'], label='Actual', marker='o', linewidth=2)
plt.plot(predictions.index, predictions_rounded, label='Predicted', marker='x', linewidth=2)
plt.fill_between(conf_int.index, conf_int['lower Value'], conf_int['upper Value'], 
                 color='gray', alpha=0.2, label='95% Confidence Interval')
plt.title('Predicted vs Actual (2021–2024)', fontsize=16)
plt.xlabel('Date')
plt.ylabel('Number of Alcohol-Related Accidents')
plt.legend()
plt.grid(True, alpha=0.3)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

