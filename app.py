import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import joblib
from flask import Flask, request, jsonify

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

# --- 2. Load the Saved Model and Preprocessors ---
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

# --- 3. Initialize the Flask App ---
app = Flask(__name__)

# --- 4. Define the Prediction Endpoint ---
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
    # ... rest of the function

    try:
        # --- 5. Preprocess the Incoming Data ---
        # This function takes the raw JSON and turns it into the 3-part
        # input our model needs.

        # 1. Env Data (Branch 1)
        env_data = [data[feature] for feature in ENV_FEATURES]
        X_env = env_scaler.transform([env_data])  # [env_data] makes it 2D

        # 2. Text Data (Branch 2)
        text_data = [data[TEXT_FEATURE]]
        X_text = text_encoder.transform(text_data)  # text_data is already a list

        # 3. Wearable Data (Branch 3)
        wearable_data = [data[feature] for feature in WEARABLE_FEATURES]
        X_wearable_scaled = wearable_scaler.transform([wearable_data])
        X_image = X_wearable_scaled.reshape(
            (-1, IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2])
        )

        # Combine into the 3-part list
        X_input = [X_env, X_text, X_image]

        # --- 6. Make the Prediction ---
        prediction = model.predict(X_input)

        # prediction[0][0] gets the single number (e.g., 8.123)
        predicted_admissions = float(prediction[0][0])

        # --- 7. Send the Response ---
        return jsonify({"predicted_hospital_admissions": predicted_admissions})

    except KeyError as e:
        return jsonify({"error": f"Missing feature in JSON data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500


# --- 8. Run the App ---
if __name__ == "__main__":
    # This starts the server on port 5000
    app.run(debug=True, host="0.0.0.0", port=5000)
