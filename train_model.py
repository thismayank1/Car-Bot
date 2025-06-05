import pandas as pd
import numpy as np
import pickle
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder

# Load the dataset
df = pd.read_csv("Cardetails.csv")

# Clean column names
df.columns = df.columns.str.strip().str.lower().str.replace(' ', '_')

# Extract brand name from 'name'
df['brand_model'] = df['name'].apply(lambda x: str(x).split()[0].lower())

# Clean mileage, engine, max_power
def extract_number(value):
    try:
        return float(str(value).split()[0])
    except:
        return np.nan

df['mileage'] = df['mileage'].apply(extract_number)
df['engine'] = df['engine'].apply(extract_number)
df['max_power'] = df['max_power'].apply(extract_number)

# Clean owner values
df['owner'] = df['owner'].str.lower().str.strip().replace({
    'first owne': 'first owner',
    'second owne': 'second owner',
    'third owne': 'third owner',
    'fourth & above owne': 'fourth & above owner'
})

# Rename 'fuel' to 'fuel_type' to match bot/model input keys
df = df.rename(columns={'fuel': 'fuel_type'})

# Drop rows with critical missing values
df.dropna(subset=['selling_price', 'mileage', 'engine', 'max_power', 'seats'], inplace=True)

# Features and target
X = df[['brand_model', 'year', 'km_driven', 'fuel_type', 'seller_type',
        'transmission', 'owner', 'mileage', 'engine', 'max_power', 'seats']]
y = df['selling_price']

# Lowercase categorical values
cat_cols = ['brand_model', 'fuel_type', 'seller_type', 'transmission', 'owner']
X.loc[:, cat_cols] = X[cat_cols].astype(str).apply(lambda col: col.str.lower())

# One-hot encode categorical variables
encoder = OneHotEncoder(handle_unknown='ignore', sparse=False)
X_cat = encoder.fit_transform(X[cat_cols])

# Combine with numeric features
X_num = X.drop(columns=cat_cols).values
X_final = np.hstack([X_num, X_cat])

# Split
X_train, X_test, y_train, y_test = train_test_split(X_final, y, test_size=0.2, random_state=42)

# Train model
model = LinearRegression()
model.fit(X_train, y_train)

# Save model and encoder
with open("model.pkl", "wb") as f:
    pickle.dump(model, f)

with open("encoder.pkl", "wb") as f:
    pickle.dump(encoder, f)

print("✅ Model and encoder saved successfully.")
print("Test R² score:", model.score(X_test, y_test))
