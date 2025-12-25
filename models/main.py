import joblib
import pandas as pd
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Load the model
model = joblib.load('sarima_alcohol_model.pkl')

app = FastAPI(title="Munich Alcohol-Related Accidents Forecast API")

class RequestBody(BaseModel):
    year: int
    month: int

@app.get("/")
def root():
    return {"message": "POST to /predict with {'year': YYYY, 'month': MM}"}

@app.post("/predict")
def predict(request: RequestBody):
    if not (1 <= request.month <= 12):
        raise HTTPException(status_code=400, detail="Month must be 1-12")
    
    target_date = pd.Timestamp(year=request.year, month=request.month, day=1)
    
    # Hardcoded last training date (Dec 2020 - change if you retrain with more data)
    last_train = pd.Timestamp('2020-12-01')
    
    if target_date <= last_train:
        raise HTTPException(status_code=400, detail=f"Date must be after {last_train.date()}")
    
    # Steps ahead
    steps = (target_date.year - last_train.year) * 12 + (target_date.month - last_train.month)
    
    forecast = model.get_forecast(steps=steps)
    pred = forecast.predicted_mean.iloc[-1]
    
    return {"prediction": round(float(pred))}