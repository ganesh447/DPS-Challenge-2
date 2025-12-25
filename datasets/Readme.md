# Data documentation — original, filtered and cleaned datasets

Three dataset files used in the project:

- Original raw export: `monatszahlen2510_verkehrsunfaelle_30_10_25.csv`
- Cleaned/normalized table used across scripts: `c_cleaned.csv`
- Model-specific filtered timeseries: `filtered_dataset.csv` (plus `training_dataset.csv` produced from it)



---

## Purpose / high-level flow

1. The raw CSV (`monatszahlen...csv`) is an export that contains monthly statistics for several accident categories (e.g. "Alkoholunfälle", "Fluchtunfälle", "Verkehrsunfälle") and subtypes (e.g. "insgesamt", "mit Personenschäden", "Verletzte und Getötete"). It contains summary rows ("Summe") and monthly rows where months are encoded like `202401` (YYYYMM).


2. `c_cleaned.csv` is a normalized, cleaned table derived from the raw export. It uses a proper date column (`DATUM` formatted as YYYY-MM-01), consistent column names and data types, and contains additional helper columns (month number, 12-month moving average, percent changes).


3. `filtered_dataset.csv` contains the single time series used for the SARIMA model: the rows from `c_cleaned.csv` filtered to Category = `Alkoholunfälle` and Type = `insgesamt`, indexed by month and with a monthly frequency set. `training_dataset.csv` is the subset used to fit the model (in the existing code, training runs up to 2020-12-01). The model file produced is `sarima_alcohol_model.pkl`.

---
