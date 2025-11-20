import requests
import json

print("--- Testing our Flask API ---")

# This is the URL where our app.py server is running
url = "http://127.0.0.1:63443/predict"
# olddd   'http://127.0.0.1:5000/predict'

# --- Create some example data for one prediction ---
# This data must match all the features our model expects.
test_data = {
    # Environmental Features
    "aqi": 150,
    "pm2_5": 80.5,
    "pm10": 120.0,
    "no2": 14.2,
    "o3": 40.1,
    "temperature": 35.5,
    "humidity": 60,
    "hospital_capacity": 1500,
    "occupancy_ratio": 0.85,
    # Text Feature
    "population_density": "Urban",
    # Wearable Features
    "heart_rate": 85.0,
    "oxygen_saturation": 95.0,
    "steps": 1500,
    "sleep_hours": 6.5,
    "respiratory_rate": 18.0,
    "body_temp": 37.1,
}

# --- Send the POST request ---
try:
    # We send our test_data as a JSON payload
    response = requests.post(url, json=test_data)

    # Check if the server responded successfully (Status Code 200)
    if response.status_code == 200:
        print("\n✅ Success! Server responded:")
        print(response.json())  # Print the JSON response from the server
    else:
        print(f"\n❌ Error: Server returned status code {response.status_code}")
        print("Response:")
        print(response.text)

except requests.exceptions.ConnectionError:
    print("\n❌ FAILED. Could not connect to the server.")
    print(f"Make sure your 'app.py' server is running in the other terminal!")
