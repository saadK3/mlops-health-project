# test_model_performance.py
"""
Comprehensive model performance testing script.
Tests the saved model on test data and validates the API endpoint.
"""
import os
import numpy as np
import pandas as pd
from tensorflow import keras
import joblib
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score
import requests
import json

# Import from train.py
from train import (
    CLIENT_CITIES,
    ENV_FEATURES,
    TEXT_FEATURE,
    WEARABLE_FEATURES,
    IMG_SHAPE,
    DATA_FILE_PATH,
    load_and_preprocess_data_for_client,
    build_multi_modal_model,
    initialize_preprocessors,
)

def test_model_loading():
    """Test if model and preprocessors can be loaded."""
    print("=" * 60)
    print("1. Testing Model and Preprocessor Loading")
    print("=" * 60)
    
    errors = []
    
    # Test model loading
    try:
        if not os.path.exists("model/health_model.keras"):
            errors.append("Model file 'model/health_model.keras' does not exist")
        else:
            model = keras.models.load_model("model/health_model.keras")
            print("✅ Model loaded successfully")
            print(f"   Model summary: {len(model.get_weights())} weight arrays")
    except Exception as e:
        errors.append(f"Model loading failed: {e}")
    
    # Test preprocessor loading
    preprocessors = {}
    for name, filename in [
        ("env_scaler", "model/env_scaler.joblib"),
        ("wearable_scaler", "model/wearable_scaler.joblib"),
        ("text_encoder", "model/text_encoder.joblib"),
    ]:
        try:
            if not os.path.exists(filename):
                errors.append(f"Preprocessor file '{filename}' does not exist")
            else:
                preprocessors[name] = joblib.load(filename)
                if preprocessors[name] is None:
                    errors.append(f"Preprocessor '{name}' loaded but is None")
                else:
                    print(f"✅ {name} loaded successfully")
        except Exception as e:
            errors.append(f"{name} loading failed: {e}")
    
    if errors:
        print("\n❌ Loading errors:")
        for error in errors:
            print(f"   - {error}")
        return None, None
    else:
        print("\n✅ All model files loaded successfully!\n")
        return model, preprocessors


def evaluate_model_on_test_data(model):
    """Evaluate the model on test data from all cities."""
    print("=" * 60)
    print("2. Evaluating Model on Test Data")
    print("=" * 60)
    
    # Initialize preprocessors (needed for data loading)
    initialize_preprocessors()
    
    all_predictions = []
    all_actuals = []
    city_results = {}
    
    for city in CLIENT_CITIES:
        try:
            print(f"\nEvaluating on {city} test data...")
            
            # Load test data for this city
            _, (X_test, y_test) = load_and_preprocess_data_for_client(city)
            
            # Make predictions
            predictions = model.predict(X_test, verbose=0)
            predictions = predictions.flatten()
            
            # Calculate metrics
            mse = mean_squared_error(y_test, predictions)
            mae = mean_absolute_error(y_test, predictions)
            rmse = np.sqrt(mse)
            r2 = r2_score(y_test, predictions)
            
            # Store results
            city_results[city] = {
                "mse": mse,
                "mae": mae,
                "rmse": rmse,
                "r2": r2,
                "samples": len(y_test),
            }
            
            # Collect for overall metrics
            all_predictions.extend(predictions)
            all_actuals.extend(y_test)
            
            print(f"   Samples: {len(y_test)}")
            print(f"   MSE: {mse:.4f}")
            print(f"   MAE: {mae:.4f}")
            print(f"   RMSE: {rmse:.4f}")
            print(f"   R²: {r2:.4f}")
            
        except Exception as e:
            print(f"   ❌ Error evaluating {city}: {e}")
            city_results[city] = {"error": str(e)}
    
    # Calculate overall metrics
    print("\n" + "-" * 60)
    print("Overall Performance (All Cities Combined):")
    print("-" * 60)
    
    overall_mse = mean_squared_error(all_actuals, all_predictions)
    overall_mae = mean_absolute_error(all_actuals, all_predictions)
    overall_rmse = np.sqrt(overall_mse)
    overall_r2 = r2_score(all_actuals, all_predictions)
    
    print(f"Total Test Samples: {len(all_actuals)}")
    print(f"MSE: {overall_mse:.4f}")
    print(f"MAE: {overall_mae:.4f}")
    print(f"RMSE: {overall_rmse:.4f}")
    print(f"R²: {overall_r2:.4f}")
    
    return city_results, {
        "mse": overall_mse,
        "mae": overall_mae,
        "rmse": overall_rmse,
        "r2": overall_r2,
        "samples": len(all_actuals),
    }


def test_api_endpoint():
    """Test the Flask API endpoint."""
    print("\n" + "=" * 60)
    print("3. Testing API Endpoint")
    print("=" * 60)
    
    url = "http://127.0.0.1:5000/predict"
    
    # Test data
    test_data = {
        "aqi": 150,
        "pm2_5": 80.5,
        "pm10": 120.0,
        "no2": 14.2,
        "o3": 40.1,
        "temperature": 35.5,
        "humidity": 60,
        "hospital_capacity": 1500,
        "occupancy_ratio": 0.85,
        "population_density": "Urban",
        "heart_rate": 85.0,
        "oxygen_saturation": 95.0,
        "steps": 1500,
        "sleep_hours": 6.5,
        "respiratory_rate": 18.0,
        "body_temp": 37.1,
    }
    
    try:
        response = requests.post(url, json=test_data, timeout=5)
        
        if response.status_code == 200:
            result = response.json()
            print("✅ API endpoint is working!")
            print(f"   Prediction: {result.get('predicted_hospital_admissions', 'N/A')}")
            return True
        else:
            print(f"❌ API returned status code {response.status_code}")
            print(f"   Response: {response.text}")
            return False
            
    except requests.exceptions.ConnectionError:
        print("⚠️  API server is not running.")
        print("   Start it with: python app.py")
        return None
    except Exception as e:
        print(f"❌ API test failed: {e}")
        return False


def print_summary(city_results, overall_results, api_test_result):
    """Print a summary of all tests."""
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    # Model performance summary
    print("\n📊 Model Performance:")
    if overall_results:
        print(f"   Overall MAE: {overall_results['mae']:.4f}")
        print(f"   Overall RMSE: {overall_results['rmse']:.4f}")
        print(f"   Overall R²: {overall_results['r2']:.4f}")
        
        # Performance thresholds (adjust based on your requirements)
        if overall_results['mae'] < 3.0 and overall_results['r2'] > 0.5:
            print("   ✅ Model performance is acceptable")
        else:
            print("   ⚠️  Model performance may need improvement")
    
    # API test summary
    print("\n🌐 API Endpoint:")
    if api_test_result is True:
        print("   ✅ API is working correctly")
    elif api_test_result is None:
        print("   ⚠️  API server not running (skipped)")
    else:
        print("   ❌ API test failed")
    
    # City-wise summary
    print("\n🏙️  City-wise Performance:")
    for city, results in city_results.items():
        if "error" not in results:
            print(f"   {city}: MAE={results['mae']:.4f}, R²={results['r2']:.4f}")
        else:
            print(f"   {city}: ❌ Error - {results['error']}")
    
    print("\n" + "=" * 60)


def main():
    """Run all tests."""
    print("\n" + "=" * 60)
    print("MODEL PERFORMANCE TEST SUITE")
    print("=" * 60)
    print()
    
    # Test 1: Model loading
    model, preprocessors = test_model_loading()
    if model is None:
        print("\n❌ Cannot proceed with tests - model loading failed")
        return
    
    # Test 2: Model evaluation
    city_results, overall_results = evaluate_model_on_test_data(model)
    
    # Test 3: API endpoint
    api_test_result = test_api_endpoint()
    
    # Print summary
    print_summary(city_results, overall_results, api_test_result)


if __name__ == "__main__":
    main()

