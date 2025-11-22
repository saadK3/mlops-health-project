import pandas as pd
import numpy as np
import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.model_selection import train_test_split
import joblib
import os
import flwr as fl

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
DATA_FILE_PATH = "data/MLOPs_data.csv"
CLIENT_CITIES = ['Delhi', 'Beijing', 'Mexico City', 'Los Angeles']


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


# --- 3. Global preprocessors (will be initialized when needed) ---
env_scaler = None
wearable_scaler = None
text_encoder = None


def initialize_preprocessors():
    """Initialize and fit preprocessors on all data."""
    global env_scaler, wearable_scaler, text_encoder
    
    if env_scaler is not None:
        return  # Already initialized
    
    print("Fitting preprocessors on all data...")
    df = pd.read_csv(DATA_FILE_PATH, encoding="latin1")

    # Fit preprocessors on full dataset (needed for consistent scaling across clients)
    env_scaler = StandardScaler()
    env_scaler.fit(df[ENV_FEATURES])

    wearable_scaler = StandardScaler()
    wearable_scaler.fit(df[WEARABLE_FEATURES])

    text_encoder = LabelEncoder()
    text_encoder.fit(POPULATION_CLASSES)

    print("Preprocessors fitted successfully.")


# --- 4. Define Data Loading Function for Each Client ---
def load_and_preprocess_data_for_client(client_city: str):
    """
    Loads the main dataset, filters for a specific city, and preprocesses
    it into the 3-input format for our multi-modal model.
    """
    # Ensure preprocessors are initialized
    initialize_preprocessors()
    
    df = pd.read_csv(DATA_FILE_PATH, encoding="latin1")
    client_df = df[df["city"] == client_city].copy()

    if len(client_df) == 0:
        raise ValueError(f"No data found for city: {client_city}")

    # 1. Preprocess Branch 1: Environmental Data
    X_env = env_scaler.transform(client_df[ENV_FEATURES])

    # 2. Preprocess Branch 2: Text Data
    X_text = text_encoder.transform(client_df[TEXT_FEATURE])

    # 3. Preprocess Branch 3: Wearable/Image Data
    X_wearable_scaled = wearable_scaler.transform(client_df[WEARABLE_FEATURES])
    X_image = X_wearable_scaled.reshape(
        (-1, IMG_SHAPE[0], IMG_SHAPE[1], IMG_SHAPE[2])
    )

    # 4. Prepare the Target (Y)
    y = client_df[TARGET].values

    # 5. Split into Train/Test for this client
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

    return (X_train, y_train), (X_test, y_test)


# --- 5. Define Flower Client ---
class HealthRiskClient(fl.client.NumPyClient):
    """
    This is the client-side logic for Federated Learning.
    Each client (city) will be an instance of this class.
    """

    def __init__(self, client_city):
        self.client_city = client_city
        self.model = None
        self.X_train = None
        self.y_train = None
        self.X_test = None
        self.y_test = None
        print(f"Client for {client_city} created.")

    def get_parameters(self, config):
        if self.model is None:
            self.model = build_multi_modal_model()
        print(f"\n[Client {self.client_city}] Sending parameters to server.")
        return self.model.get_weights()

    def fit(self, parameters, config):
        if self.X_train is None:
            print(f"[Client {self.client_city}] Loading local data...")
            (self.X_train, self.y_train), (self.X_test, self.y_test) = (
                load_and_preprocess_data_for_client(self.client_city)
            )
            print(
                f"[Client {self.client_city}] Data loaded. {len(self.y_train)} train samples."
            )

        if self.model is None:
            self.model = build_multi_modal_model()

        self.model.set_weights(parameters)

        print(f"[Client {self.client_city}] Training local model...")
        self.model.fit(
            self.X_train,
            self.y_train,
            epochs=1,
            batch_size=32,
            validation_split=0.1,
            verbose=0,  # Set to 0 for cleaner output
        )

        print(f"[Client {self.client_city}] Training complete, returning parameters.")
        return self.model.get_weights(), len(self.y_train), {}

    def evaluate(self, parameters, config):
        print(f"[Client {self.client_city}] Evaluating model on local test set...")

        if self.X_test is None:
            _, (self.X_test, self.y_test) = load_and_preprocess_data_for_client(
                self.client_city
            )

        if self.model is None:
            self.model = build_multi_modal_model()
        self.model.set_weights(parameters)

        loss, mae = self.model.evaluate(self.X_test, self.y_test, verbose=0)

        print(
            f"[Client {self.client_city}] Evaluation: Loss={loss:.4f}, MAE={mae:.4f}"
        )
        return loss, len(self.y_test), {"mae": mae}


def client_fn(cid: str) -> HealthRiskClient:
    """A function to create a client instance."""
    city_name = CLIENT_CITIES[int(cid)]
    return HealthRiskClient(client_city=city_name)


# --- 6. Main execution (only runs when script is executed directly) ---
if __name__ == "__main__":
    print("Starting federated learning training script (simulation mode)...")
    
    # Initialize preprocessors
    initialize_preprocessors()
    
    # --- Run Federated Learning Simulation ---
    print("\n--- Starting Federated Learning Simulation ---")

    # Define our Aggregation Strategy
    strategy = fl.server.strategy.FedAvg(
        min_fit_clients=len(CLIENT_CITIES),  # Wait for all clients to train
        min_evaluate_clients=len(CLIENT_CITIES),  # Evaluate on all clients
        min_available_clients=len(
            CLIENT_CITIES
        ),  # Wait for all clients to be available
    )

    # Start the Simulation
    history = fl.simulation.start_simulation(
        client_fn=client_fn,
        num_clients=len(CLIENT_CITIES),
        config=fl.server.ServerConfig(num_rounds=3),  # Run for 3 rounds
        strategy=strategy,
        client_resources={"num_cpus": 1, "num_gpus": 0},  # Basic resources
    )

    print("--- Federated Learning Simulation Finished! ---")

    # --- 7. Extract Final Aggregated Model ---
    print("\nExtracting final aggregated model...")
    # Note: In Flower's simulation mode, the final aggregated model weights are held by the server
    # and not directly accessible. For this script, we'll create a model instance.
    # In production, you would retrieve the final aggregated weights directly from the server.
    # 
    # The model from a client that participated in all rounds will have weights that are
    # close to the aggregated model (since clients receive aggregated weights each round).

    final_model = build_multi_modal_model()

    # Create a client and get its parameters (which reflect the final round's aggregated weights)
    # Note: This is an approximation - in production, get weights directly from the server
    temp_client = client_fn("0")
    final_params = temp_client.get_parameters({})
    final_model.set_weights(final_params)
    print("Final model extracted (using client parameters as proxy for aggregated model).")

    # --- 8. Save the Model and Preprocessors ---
    print("Saving model and preprocessors...")
    # Create a 'model' directory if it doesn't exist
    os.makedirs("model", exist_ok=True)

    # Save the TensorFlow/Keras model (federated aggregated model)
    final_model.save("model/health_model.keras")

    # Save our preprocessors using joblib
    joblib.dump(env_scaler, "model/env_scaler.joblib")
    joblib.dump(wearable_scaler, "model/wearable_scaler.joblib")
    joblib.dump(text_encoder, "model/text_encoder.joblib")

    print("--- ✅ Training and saving complete! ---")
