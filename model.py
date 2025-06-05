import pickle
import numpy as np
import pandas as pd

# Load trained model and encoder
model = pickle.load(open("model.pkl", "rb"))
encoder = pickle.load(open("encoder.pkl", "rb"))

# Columns that were one-hot encoded
cat_cols = ['brand_model', 'fuel_type', 'seller_type', 'transmission', 'owner']

def clean_input(data):
    """
    Cleans and prepares a dictionary of input data for prediction.
    Expects keys: brand_model, year, km_driven, fuel_type, seller_type,
                  transmission, owner, mileage, engine, max_power, seats
    """
    # Lowercase all categorical fields
    for key in cat_cols:
        data[key] = str(data.get(key, "")).lower().strip()

    # Clean numeric-like strings
    def to_float(value):
        try:
            return float(str(value).split()[0])
        except:
            return 0.0

    data['mileage'] = to_float(data.get('mileage', 0))
    data['engine'] = to_float(data.get('engine', 0))
    data['max_power'] = to_float(data.get('max_power', 0))
    data['km_driven'] = int(data.get('km_driven', 0))
    data['year'] = int(data.get('year', 2000))
    data['seats'] = int(data.get('seats', 5))

    return data

def predict_car_price(data):
    # Clean and prepare input
    data = clean_input(data)
    df = pd.DataFrame([data])

    # Encode categorical features
    X_cat = encoder.transform(df[cat_cols])

    # Select numerical columns
    num_cols = ['year', 'km_driven', 'mileage', 'engine', 'max_power', 'seats']
    X_num = df[num_cols].values

    # Final input vector
    X_final = np.hstack([X_num, X_cat])

    # Predict
    prediction = model.predict(X_final)[0]
    return round(prediction, 2)
