import os
import numpy as np
import tensorflow as tf
from tensorflow import keras
import joblib
from flask import Flask, request, jsonify

print("--- Starting Flask API Server ---")

# --- 1. Define Global Configuration (must match train.py) ---
ENV_FEATURES = [
    'aqi', 'pm2_5', 'pm10', 'no2', 'o3', 'temperature', 
    'humidity', 'hospital_capacity', 'occupancy_ratio'
]
TEXT_FEATURE = 'population_density'
WEARABLE_FEATURES = [
    'heart_rate', 'oxygen_saturation', 'steps', 
    'sleep_hours', 'respiratory_rate', 'body_temp'
]
IMG_SHAPE = (2, 3, 1)

# --- 2. Load the Saved Model and Preprocessors ---
print("Loading model and preprocessors...")
try:
    model = keras.models.load_model('model/health_model.keras')
    env_scaler = joblib.load('model/env_scaler.joblib')
    wearable_scaler = joblib.load('model/wearable_scaler.joblib')
    text_encoder = joblib.load('model/text_encoder.joblib')
    print("✅ Model and preprocessors loaded successfully.")
except Exception as e:
    print(f"--- ERROR: Could not load model or preprocessors. ---")
    print(f"Make sure you have run train.py first!")
    print(f"Error: {e}")
    model = None # Set to None so we know there's a problem

# --- 3. Initialize the Flask App ---
app = Flask(__name__) # This creates our web app

# --- 4. Define the Prediction Endpoint ---
# This creates a URL for our server, e.g., http://localhost:5000/predict
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model is not loaded. Check server logs."}), 500

    # Get the JSON data sent by the user
    data = request.get_json()

    try:
        # --- 5. Preprocess the Incoming Data ---
        # This function takes the raw JSON and turns it into the 3-part
        # input our model needs.
        
        # 1. Env Data (Branch 1)
        env_data = [data[feature] for feature in ENV_FEATURES]
        X_env = env_scaler.transform([env_data]) # [env_data] makes it 2D
        
        # 2. Text Data (Branch 2)
        text_data = [data[TEXT_FEATURE]]
        X_text = text_encoder.transform(text_data) # text_data is already a list
        
        # 3. Wearable Data (Branch 3)
        wearable_data = [data[feature] for feature in WEARABLE_FEATURES]
        X_wearable_scaled = wearable_scaler.transform([wearable_data])
        X_image = X_wearable_scaled.reshape((-1, IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2]))

        # Combine into the 3-part list
        X_input = [X_env, X_text, X_image]

        # --- 6. Make the Prediction ---
        prediction = model.predict(X_input)
        
        # prediction[0][0] gets the single number (e.g., 8.123)
        predicted_admissions = float(prediction[0][0])

        # --- 7. Send the Response ---
        return jsonify({
            'predicted_hospital_admissions': predicted_admissions
        })

    except KeyError as e:
        return jsonify({"error": f"Missing feature in JSON data: {str(e)}"}), 400
    except Exception as e:
        return jsonify({"error": f"An error occurred: {str(e)}"}), 500

# --- 8. Run the App ---
if __name__ == '__main__':
    # This starts the server on port 5000
    app.run(debug=True, host='0.0.0.0', port=5000)