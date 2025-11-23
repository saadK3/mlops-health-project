"""
Simplified training script that trains a model directly without federated learning.
This avoids the TensorFlow DLL issues with Flower simulation.
"""
import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os

# --- 1. Define Global Configuration ---
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
POPULATION_CLASSES = ["Rural", "Urban", "Suburban"]
WEARABLE_FEATURES = [
    "heart_rate",
    "oxygen_saturation",
    "steps",
    "sleep_hours",
    "respiratory_rate",
    "body_temp",
]
TARGET = "hospital_admissions"
IMG_SHAPE = (2, 3, 1)
DATA_FILE_PATH = "data/MLOPs_data.csv"


# --- 2. Define the Model Building Function ---
def build_multi_modal_model():
    input_env = layers.Input(shape=(len(ENV_FEATURES),), name="env_input")
    x_env = layers.Dense(32, activation="relu")(input_env)
    x_env = layers.Dropout(0.3)(x_env)
    x_env_out = layers.Dense(16, activation="relu")(x_env)

    input_text = layers.Input(shape=(1,), name="text_input")
    x_text = layers.Embedding(input_dim=len(POPULATION_CLASSES), output_dim=4)(
        input_text
    )
    x_text = layers.Flatten()(x_text)
    x_text_out = layers.Dense(4, activation="relu")(x_text)

    input_image = layers.Input(shape=IMG_SHAPE, name="wearable_image_input")
    x_img = layers.Conv2D(8, (2, 2), activation="relu", padding="same")(input_image)
    x_img = layers.MaxPooling2D((1, 1))(x_img)
    x_img = layers.Flatten()(x_img)
    x_img_out = layers.Dense(8, activation="relu")(x_img)

    concatenated = layers.concatenate([x_env_out, x_text_out, x_img_out])

    x = layers.Dense(32, activation="relu")(concatenated)
    x = layers.Dropout(0.5)(x)
    output_layer = layers.Dense(1, activation="linear", name="output")(x)

    model = keras.Model(
        inputs=[input_env, input_text, input_image],
        outputs=output_layer,
        name="3_branch_health_model",
    )
    model.compile(loss="mse", optimizer="adam", metrics=["mae"])
    return model


# --- 3. Main Training Function ---
def main():
    print("=" * 60)
    print("Simplified Training Script (No Federated Learning)")
    print("=" * 60)
    
    # Load data
    print("\n1. Loading data...")
    if not os.path.exists(DATA_FILE_PATH):
        raise FileNotFoundError(f"Data file not found: {DATA_FILE_PATH}")
    
    df = pd.read_csv(DATA_FILE_PATH, encoding="latin1")
    print(f"   ✅ Loaded {len(df)} rows")
    
    # Initialize and fit preprocessors
    print("\n2. Fitting preprocessors...")
    env_scaler = StandardScaler()
    env_scaler.fit(df[ENV_FEATURES])
    
    wearable_scaler = StandardScaler()
    wearable_scaler.fit(df[WEARABLE_FEATURES])
    
    text_encoder = LabelEncoder()
    text_encoder.fit(POPULATION_CLASSES)
    print("   ✅ Preprocessors fitted")
    
    # Preprocess data
    print("\n3. Preprocessing data...")
    X_env = env_scaler.transform(df[ENV_FEATURES])
    X_text = text_encoder.transform(df[TEXT_FEATURE])
    X_wearable_scaled = wearable_scaler.transform(df[WEARABLE_FEATURES])
    X_image = X_wearable_scaled.reshape((-1, IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2]))
    
    y = df[TARGET].values
    
    # Split data
    indices = np.arange(len(y))
    train_indices, test_indices = train_test_split(
        indices, test_size=0.2, random_state=42
    )
    
    X_train = [
        X_env[train_indices],
        X_text[train_indices],
        X_image[train_indices],
    ]
    y_train = y[train_indices]
    
    X_test = [
        X_env[test_indices],
        X_text[test_indices],
        X_image[test_indices],
    ]
    y_test = y[test_indices]
    
    print(f"   ✅ Train: {len(y_train)} samples, Test: {len(y_test)} samples")
    
    # Build and train model
    print("\n4. Building model...")
    model = build_multi_modal_model()
    print("   ✅ Model built")
    
    print("\n5. Training model...")
    print("   (This may take a few minutes...)")
    history = model.fit(
        X_train,
        y_train,
        epochs=10,
        batch_size=32,
        validation_data=(X_test, y_test),
        verbose=1,
    )
    
    # Evaluate
    print("\n6. Evaluating model...")
    loss, mae = model.evaluate(X_test, y_test, verbose=0)
    print(f"   ✅ Test Loss: {loss:.4f}, Test MAE: {mae:.4f}")
    
    # Save model and preprocessors
    print("\n7. Saving model and preprocessors...")
    os.makedirs("model", exist_ok=True)
    
    model.save("model/health_model.keras")
    joblib.dump(env_scaler, "model/env_scaler.joblib")
    joblib.dump(wearable_scaler, "model/wearable_scaler.joblib")
    joblib.dump(text_encoder, "model/text_encoder.joblib")
    
    print("   ✅ Model saved to model/health_model.keras")
    print("   ✅ Preprocessors saved to model/ directory")
    
    print("\n" + "=" * 60)
    print("✅ Training complete!")
    print("=" * 60)


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        raise

