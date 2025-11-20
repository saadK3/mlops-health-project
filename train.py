import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler, LabelEncoder
import joblib
import os
from tensorflow.keras.callbacks import EarlyStopping  # <--- 1. IMPORT IT HERE

print("Starting training script (v2 with EarlyStopping)...")

# --- 1. Define Global Configuration (from our EDA) ---
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
DATA_FILE_PATH = "C:\\Users\\admin\\Desktop\\mlops-health-project\\data\\MLOPs_data.csv"


# --- 2. Define the Model Building Function (copied from our notebook) ---
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


# --- 3. Load ALL Data and Preprocess ---
print("Loading and preprocessing all data for final training...")
df = pd.read_csv(DATA_FILE_PATH, encoding="latin1")

# Fit and save the preprocessors
env_scaler = StandardScaler()
X_env = env_scaler.fit_transform(df[ENV_FEATURES])

wearable_scaler = StandardScaler()
X_wearable_scaled = wearable_scaler.fit_transform(df[WEARABLE_FEATURES])
X_image = X_wearable_scaled.reshape((-1, IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2]))

text_encoder = LabelEncoder()
X_text = text_encoder.fit_transform(df[TEXT_FEATURE])

y = df[TARGET].values

# Prepare the 3-part input list
X_train = [X_env, X_text, X_image]
y_train = y

# --- 4. Train the Final Global Model (UPDATED) ---
print("Training the final global model...")
model = build_multi_modal_model()

# --- THIS IS THE CHANGE ---
# Define our EarlyStopping callback
# It will monitor 'val_loss' (our "real exam" score)
# patience=5 means it will wait 5 epochs for the score to improve before stopping
# restore_best_weights=True is the magic: it saves the model from the "sweet spot"
early_stopper = EarlyStopping(
    monitor="val_loss", patience=5, verbose=1, restore_best_weights=True
)

# We set epochs to a high number (like 100) and let EarlyStopping
# find the best one and stop for us.
model.fit(
    X_train,
    y_train,
    epochs=50,  # Set a high number
    batch_size=64,
    validation_split=0.2,  # Use 20% of data for validation
    verbose=1,
    callbacks=[early_stopper],
)  # <-- Add the callback here

print("Training finished. Best model weights have been restored.")
# --- END OF CHANGE ---

# --- 5. Save the Model and Preprocessors ---
print("Saving model and preprocessors...")
# Create a 'model' directory if it doesn't exist
os.makedirs("model", exist_ok=True)

# Save the TensorFlow/Keras model (this will now be the BEST model)
model.save("model/health_model.keras")

# Save our preprocessors using joblib
joblib.dump(env_scaler, "model/env_scaler.joblib")
joblib.dump(wearable_scaler, "model/wearable_scaler.joblib")
joblib.dump(text_encoder, "model/text_encoder.joblib")

print("--- ✅ Training and saving complete! ---")
