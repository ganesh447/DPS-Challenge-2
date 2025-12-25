# DPS Challenge — Munich Traffic Accidents (SARIMA forecast)

Repository: ganesh447/DPS-Challenge-2  
Challenge: [Open Data Portal — DPS Challenge](https://dps-challenge-front.netlify.app/opendataportal)

This repository contains the code and artifacts used to build a SARIMA model forecasting monthly counts of alcohol-related traffic accidents and supporting EDA / preprocessing notebooks and CSV exports.

---

## Project structure 

- `forecast.py`                — training script (fits SARIMA on training period and saves model as `sarima_alcohol_model.pkl`)
- main.py — FastAPI app that loads `sarima_alcohol_model.pkl` and exposes a /predict endpoint.
- `Performance_evaluation.py`               — evaluation pipeline (computes metrics and creates `predicted_vs_actual.png`)
- `sarima_alcohol_model.pkl`    — saved SARIMA model (output produced by `forecast.py`)
- Datasets/
- `c_cleaned.csv`              — cleaned & normalized dataset (master cleaned table)
- `filtered_dataset.csv`        — filtered time series used for modelling (Category = `Alkoholunfälle`, Type = `insgesamt`)
- `training_dataset.csv`        — subset of `filtered_dataset.csv` used for model training (up to 2020-12-01 in current scripts)
- `motnatszahlen...csv`         — original raw export (monthly export with "Summe" rows and YYYYMM month encoding)
- models                      — Model training files and plots
  - `sarima_alcohol_model.pkl` 
  - `forecast.py`  
  - `1_step_ahead_forecast.png`
  - `ACF_PACF.png`
  - `Training_data.png`
- evaluation/                  — evaluation artifacts 
  - `Performance_evaluation.py`
  - `Model_pefrormance.png`
- notebooks/                   — Jupyter notebooks (EDA, exploration)
  - `EDA_Munich_Accident.ipynb`  — exploratory analysis used during the project
- requirements.txt             —  Python packages

---

## Model training & artifact

- Script: `forecast.py`
  - Reads `datasets/c_cleaned.csv`, filters to alcohol-related accidents (Category=`Alkoholunfälle`, Type=`insgesamt`), resamples/sets frequency to monthly (`MS`) and splits train up to `2020-12-01`.
  - Fits a SARIMAX model (the current settings in the script: order=(1,1,1), seasonal_order=(1,1,1,12)).
  - Saves the fitted model with joblib to `sarima_alcohol_model.pkl`.
  - Prints model summary and plots a one-step forecast for Jan 2021 (and shows CI).

- Model file: `sarima_alcohol_model.pkl` — joblib serialized fitted model object. Keep alongside `main.py` (or update `main.py`'s load path).

---

## Evaluation & figure

- Script: `Performance_evaluation.py` loads model and test data, computes metrics (MAE, MSE, RMSE, R², MAPE), and produces a Predicted vs Actual plot with 95% CI.

---

## API (FastAPI) — main.py

- Purpose: Serve forecasts via HTTP.
- Key behavior (current implementation):
  - Loads `sarima_alcohol_model.pkl` at startup.
  - POST /predict accepts JSON: { "year": YYYY, "month": M }.
  - Validates that the requested date is after the training last date (script uses last_train = 2020-12-01).
  - Computes steps ahead and returns the predicted mean for that date.

- API: `https://dps-challenge-2.onrender.com/predict`

---

## How to run this project locally

Prerequisites
- Python 3.8+ recommended
- git

1. Clone the repo
```bash
git clone https://github.com/ganesh447/DPS-Challenge-2.git
cd DPS-Challenge-2
```

2. Create and activate a virtual environment
```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate
```

3. Install dependencies
- If `requirements.txt` exists:
```bash
pip install -r requirements.txt
```
- If not, install the packages used in the scripts:
```bash
pip install pandas numpy matplotlib seaborn statsmodels joblib jupyterlab
```

4. Inspect datasets
- `monatszahlen...csv` — raw export
- `c_cleaned.csv` — cleaned/normalized table
- `filtered_dataset.csv` — model input time-series (Alkoholunfälle, insgesamt)

5. Run the training script (fits SARIMA and saves model)
```bash
python forecast.py
```
Expected outputs:
- `sarima_alcohol_model.pkl` (model saved with joblib)
- console output with model summary and a plotted forecast figure

Notes:
- The current `forecast.py` reads `datasets/c_cleaned.csv`. Ensure the file path referenced in the script matches the local layout. 

6. Run evaluation 
```bash
python evaluate.py
```
Expected outputs:
- Numeric metrics printed (MAE, MSE, RMSE, R², MAPE)
- `evaluation/predicted_vs_actual.png` (or `predicted_vs_actual.png`) produced in the evaluation folder

7. Run the API (FastAPI) — serves the trained model
- Ensure `sarima_alcohol_model.pkl` is present in repo root (or update `main.py` to the correct path).
- Run with uvicorn:
```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- Example request:
POST http://127.0.0.1:8000/predict
JSON body:
```json
{"year": 2021, "month": 1}
```
