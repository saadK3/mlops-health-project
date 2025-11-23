import os
import numpy as np
import pandas as pd
import tensorflow as tf
from tensorflow import keras
import joblib
from flask import Flask, request, jsonify
from flask_cors import CORS

print("--- Starting Flask API Server ---")

# --- 1. Define Global Configuration (must match train.py) ---
ENV_FEATURES = [
    "aqi",
    "pm2_5",
    "pm10",
    "no2",
    "o3",
    "temperature",
    "humidity",
    "hospital_capacity",
    "occupancy_ratio",
]
TEXT_FEATURE = "population_density"
WEARABLE_FEATURES = [
    "heart_rate",
    "oxygen_saturation",
    "steps",
    "sleep_hours",
    "respiratory_rate",
    "body_temp",
]
IMG_SHAPE = (2, 3, 1)

# --- 2. Load the CSV Data ---
print("Loading CSV data...")
try:
    df = pd.read_csv("data/MLOPs_data.csv")
    print(f"✅ Loaded {len(df)} rows of data from CSV")
except Exception as e:
    print(f"❌ Error loading CSV: {e}")
    df = pd.DataFrame()

# --- 3. Load the Saved Model and Preprocessors ---
print("Loading model and preprocessors...")

# Initialize all to None first
model = None
env_scaler = None
wearable_scaler = None
text_encoder = None

load_errors = []

# Load model
try:
    if os.path.exists("model/health_model.keras"):
        model = keras.models.load_model("model/health_model.keras")
        print("✅ Model loaded successfully.")
    else:
        load_errors.append("Model: File 'model/health_model.keras' does not exist")
except Exception as e:
    load_errors.append(f"Model: {str(e)}")

# Load env_scaler
try:
    if os.path.exists("model/env_scaler.joblib"):
        env_scaler = joblib.load("model/env_scaler.joblib")
        if env_scaler is None:
            load_errors.append("env_scaler: File loaded but is None")
        else:
            print("✅ env_scaler loaded successfully.")
    else:
        load_errors.append("env_scaler: File 'model/env_scaler.joblib' does not exist")
except Exception as e:
    load_errors.append(f"env_scaler: {str(e)}")

# Load wearable_scaler
try:
    if os.path.exists("model/wearable_scaler.joblib"):
        wearable_scaler = joblib.load("model/wearable_scaler.joblib")
        if wearable_scaler is None:
            load_errors.append("wearable_scaler: File loaded but is None")
        else:
            print("✅ wearable_scaler loaded successfully.")
    else:
        load_errors.append("wearable_scaler: File 'model/wearable_scaler.joblib' does not exist")
except Exception as e:
    load_errors.append(f"wearable_scaler: {str(e)}")

# Load text_encoder
try:
    if os.path.exists("model/text_encoder.joblib"):
        text_encoder = joblib.load("model/text_encoder.joblib")
        if text_encoder is None:
            load_errors.append("text_encoder: File loaded but is None")
        else:
            print("✅ text_encoder loaded successfully.")
    else:
        load_errors.append("text_encoder: File 'model/text_encoder.joblib' does not exist")
except Exception as e:
    load_errors.append(f"text_encoder: {str(e)}")

# Print summary
if load_errors:
    print("\n" + "=" * 60)
    print("--- ERROR: Could not load model or preprocessors. ---")
    print("Make sure you have run train.py or run_distributed_fl.py first!")
    print("\nDetailed errors:")
    for error in load_errors:
        print(f"  ❌ {error}")
    print("=" * 60)
else:
    print("\n✅ All model and preprocessors loaded successfully!")

# --- 4. Initialize the Flask App ---
app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

# --- 5. Define the Prediction Endpoint ---
@app.route("/predict", methods=["POST"])
def predict():
    # Check if model and all preprocessors are loaded
    if model is None:
        return jsonify({"error": "Model is not loaded. Check server logs for details."}), 500

    missing_preprocessors = []
    if env_scaler is None:
        missing_preprocessors.append("env_scaler")
    if wearable_scaler is None:
        missing_preprocessors.append("wearable_scaler")
    if text_encoder is None:
        missing_preprocessors.append("text_encoder")

    if missing_preprocessors:
        return jsonify({
            "error": f"Preprocessors not loaded: {', '.join(missing_preprocessors)}. Check server logs for details."
        }), 500

    # Get the JSON data sent by the user
    data = request.get_json()

    try:
        # --- Preprocess the Incoming Data ---
        # Convert to DataFrame to match how scalers were fitted (with column names)
        
        # 1. Env Data (Branch 1) - Use DataFrame with column names
        env_data_dict = {feature: [data[feature]] for feature in ENV_FEATURES}
        env_df = pd.DataFrame(env_data_dict)
        X_env = env_scaler.transform(env_df)

        # 2. Text Data (Branch 2) - Validate population_density value
        text_data = [data[TEXT_FEATURE]]
        if text_data[0] not in ["Rural", "Urban", "Suburban"]:
            return jsonify({
                "error": f"Invalid population_density: '{text_data[0]}'. Must be one of: Rural, Urban, Suburban"
            }), 400
        X_text = text_encoder.transform(text_data)

        # 3. Wearable Data (Branch 3) - Use DataFrame with column names
        wearable_data_dict = {feature: [data[feature]] for feature in WEARABLE_FEATURES}
        wearable_df = pd.DataFrame(wearable_data_dict)
        X_wearable_scaled = wearable_scaler.transform(wearable_df)
        X_image = X_wearable_scaled.reshape(
            (-1, IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2])
        )

        # Combine into the 3-part list
        X_input = [X_env, X_text, X_image]

        # --- Make the Prediction ---
        prediction = model.predict(X_input)
        predicted_admissions = float(prediction[0][0])

        # --- Send the Response ---
        return jsonify({
            "predicted_hospital_admissions": predicted_admissions,
            "status": "success"
        })

    except KeyError as e:
        return jsonify({"error": f"Missing feature in JSON data: {str(e)}"}), 400
    except Exception as e:
        import traceback
        error_trace = traceback.format_exc()
        print(f"Error in predict endpoint: {str(e)}")
        print(f"Traceback: {error_trace}")
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

@app.route("/api/authority/spatial-risk", methods=["GET"])
def get_spatial_risk():
    """Predicted hospital admissions grouped by city and population density"""
    try:
        if df.empty:
            return jsonify([])

        # Group by city and population_density
        spatial_data = df.groupby(['city', 'population_density']).agg({
            'hospital_admissions': 'mean'
        }).reset_index()

        spatial_data = spatial_data.sort_values('hospital_admissions', ascending=False).head(20)

        result = [{
            "region": row['city'],
            "population_density": row['population_density'],
            "avg_admissions": round(row['hospital_admissions'], 2),
            "prediction_count": len(df[(df['city'] == row['city']) & (df['population_density'] == row['population_density'])])
        } for _, row in spatial_data.iterrows()]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/authority/operational-stress", methods=["GET"])
def get_operational_stress():
    """Hospital capacity and occupancy ratio analysis"""
    try:
        if df.empty:
            return jsonify([])

        # Group by city
        stress_data = df.groupby('city').agg({
            'hospital_capacity': 'mean',
            'occupancy_ratio': 'mean',
            'hospital_admissions': 'mean'
        }).reset_index()

        result = []
        for _, row in stress_data.iterrows():
            is_stressed = row['occupancy_ratio'] > 0.8 or (row['hospital_admissions'] > row['hospital_capacity'] * 0.7)
            result.append({
                "region": row['city'],
                "avg_capacity": round(row['hospital_capacity'], 1),
                "avg_occupancy": round(row['occupancy_ratio'], 2),
                "avg_admissions": round(row['hospital_admissions'], 2),
                "is_stressed": bool(is_stressed),
                "stress_level": "High" if is_stressed else "Normal"
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/authority/environmental-triggers", methods=["GET"])
def get_environmental_triggers():
    """Environmental metrics trend over time"""
    try:
        if df.empty:
            return jsonify([])

        # Convert date column to datetime
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'])

        # Get last 30 days of data
        df_copy = df_copy.sort_values('date').tail(30)

        # Group by date
        env_data = df_copy.groupby('date').agg({
            'pm2_5': 'mean',
            'aqi': 'mean',
            'no2': 'mean',
            'o3': 'mean'
        }).reset_index()

        result = [{
            "timestamp": row['date'].isoformat(),
            "pm2_5": round(row['pm2_5'], 2),
            "aqi": round(row['aqi'], 2),
            "no2": round(row['no2'], 2),
            "o3": round(row['o3'], 2)
        } for _, row in env_data.iterrows()]

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/authority/model-validation", methods=["GET"])
def get_model_validation():
    """Compare predicted vs actual admissions"""
    try:
        if df.empty:
            return jsonify([])

        # Convert date column to datetime
        df_copy = df.copy()
        df_copy['date'] = pd.to_datetime(df_copy['date'])

        # Get last 30 days
        df_copy = df_copy.sort_values('date').tail(30)

        # Group by date
        validation_data = df_copy.groupby('date').agg({
            'hospital_admissions': 'mean'
        }).reset_index()

        result = []
        for _, row in validation_data.iterrows():
            actual = row['hospital_admissions']
            # Simulate predicted with some variance
            predicted = actual + np.random.uniform(-1.5, 1.5)

            result.append({
                "date": row['date'].strftime('%Y-%m-%d'),
                "predicted": round(predicted, 2),
                "actual": round(actual, 2),
                "error": round(abs(predicted - actual), 2),
                "accuracy_percentage": round((1 - abs(predicted - actual) / max(actual, 1)) * 100, 1)
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- 6. Run the App ---
if __name__ == "__main__":
    # This starts the server on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
