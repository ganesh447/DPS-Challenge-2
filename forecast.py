import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

df = pd.read_csv('c_cleaned.csv', parse_dates=['DATUM'], index_col='DATUM')
filtered_df = df[(df['Category'] == 'Alkoholunfälle') & (df['Type'] == 'insgesamt')].copy()
filtered_df = filtered_df.sort_index()
ts = filtered_df['Value']
ts = ts.asfreq('MS')
train = ts.loc[:'2020-12-01']  # (Jan 2000 to Dec 2020)

print("Training data shape:", train.shape)


plt.figure(figsize=(12, 6))
plt.plot(train)
plt.title('Alcohol-Related Accidents (insgesamt) - Training Data')
plt.xlabel('Date')
plt.ylabel('Number of Accidents')
plt.grid(True)
plt.show()

# ACF and PACF for parameter hints
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
plot_acf(train, ax=axes[0], lags=36)  # Up to 3 years
plot_pacf(train, ax=axes[1], lags=36)
plt.show()

from statsmodels.tsa.statespace.sarimax import SARIMAX

# model fitting
model = SARIMAX(train,
                order=(1, 1, 1),                # Non-seasonal: AR(1), diff(1), MA(1)
                seasonal_order=(1, 1, 1, 12),   # Seasonal: AR(1), diff(1), MA(1), period=12
                enforce_stationarity=False,
                enforce_invertibility=False)

fitted_model = model.fit(disp=False)  

# Model summary 
print(fitted_model.summary())

# Forecasting 1 month ahead
forecast = fitted_model.get_forecast(steps=1)
predicted_value = forecast.predicted_mean
conf_int = forecast.conf_int(alpha=0.05)  

print("Forecast for January 2021:", predicted_value)
print("95% Confidence Interval:\n", conf_int)

# Plotting forecast with historical data
plt.figure(figsize=(12, 6))
plt.plot(train, label='Historical Data')
plt.plot(forecast.predicted_mean, label='Forecast', marker='o')
plt.fill_between(conf_int.index, conf_int.iloc[:, 0], conf_int.iloc[:, 1], color='gray', alpha=0.3, label='95% CI')
plt.title('SARIMA Forecast for Alcohol-Related Accidents (Jan 2021)')
plt.xlabel('Date')
plt.ylabel('Number of Accidents')
plt.legend()
plt.grid(True)
plt.show()