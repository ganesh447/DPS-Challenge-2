import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load the pre-trained model (ensure 'sarima_alcohol_model.pkl' is in the same directory)
model = joblib.load('sarima_alcohol_model.pkl')

app = FastAPI(
    title="Munich Alcohol-Related Accidents Forecast API",
    description="SARIMA model predicting monthly 'Alkoholunfälle' (insgesamt)"
)

class RequestBody(BaseModel):
    year: int
    month: int  # 1-12

@app.get("/")
def root():
    return {"message": "POST to /predict with {'year': YYYY, 'month': MM}"}

@app.post("/predict")
def predict(request: RequestBody):
    if not (1 <= request.month <= 12):
        raise HTTPException(status_code=400, detail="Month must be 1-12")
    
    target_date = pd.Timestamp(year=request.year, month=request.month, day=1)
    last_train = model.data.endog_dates[-1]  # Last training date from fitted model
    
    if target_date <= pd.Timestamp(last_train):
        raise HTTPException(status_code=400, detail="Date must be in the future")
    
    # Steps ahead
    steps = (target_date.year - last_train.year) * 12 + (target_date.month - last_train.month)
    
    forecast = model.get_forecast(steps=steps)
    pred = forecast.predicted_mean.iloc[-1]
    
    return {"prediction": round(float(pred))}