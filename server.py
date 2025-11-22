"""
Federated Learning Server
Runs on the central server and coordinates the federated learning process.
"""
import flwr as fl
import argparse
import sys
import os
import joblib

# Import shared configuration and utilities
import train
from train import (
    CLIENT_CITIES,
    build_multi_modal_model,
    initialize_preprocessors,
)

def main():
    parser = argparse.ArgumentParser(
        description="Federated Learning Server for Health Risk Prediction"
    )
    parser.add_argument(
        "--port",
        type=int,
        default=9090,
        help="Port number for the server (default: 9090)",
    )
    parser.add_argument(
        "--rounds",
        type=int,
        default=3,
        help="Number of federated learning rounds (default: 3)",
    )
    parser.add_argument(
        "--min-clients",
        type=int,
        default=len(CLIENT_CITIES),
        help=f"Minimum number of clients required (default: {len(CLIENT_CITIES)})",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("Federated Learning Server")
    print("=" * 60)
    print(f"Server will listen on port: {args.port}")
    print(f"Number of FL rounds: {args.rounds}")
    print(f"Minimum clients required: {args.min_clients}")
    print(f"Expected clients: {CLIENT_CITIES}")
    print("=" * 60)
    print("\nWaiting for clients to connect...\n")

    # Custom strategy that saves model after final round
    class FedAvgWithSave(fl.server.strategy.FedAvg):
        def aggregate_fit(self, server_round, results, failures):
            """Override to save model after final round."""
            aggregated = super().aggregate_fit(server_round, results, failures)
            if aggregated is not None and server_round == args.rounds:
                # Get the aggregated parameters (Flower Parameters object)
                aggregated_parameters = aggregated[0]
                
                # Convert Flower Parameters to numpy arrays
                import flwr.common
                parameters_ndarrays = flwr.common.parameters_to_ndarrays(aggregated_parameters)
                
                # Save the model
                print("\n" + "=" * 60)
                print(" Saving aggregated model...")
                print("=" * 60)
                try:
                    # Initialize preprocessors
                    initialize_preprocessors()
                    
                    # Get preprocessors from train module after initialization
                    # (they are set as global variables in train.py)
                    env_scaler = train.env_scaler
                    wearable_scaler = train.wearable_scaler
                    text_encoder = train.text_encoder
                    
                    # Verify preprocessors are initialized
                    if env_scaler is None or wearable_scaler is None or text_encoder is None:
                        raise ValueError("Preprocessors were not initialized properly")
                    
                    # Build model and set aggregated weights
                    model = build_multi_modal_model()
                    model.set_weights(parameters_ndarrays)
                    
                    # Create model directory
                    os.makedirs("model", exist_ok=True)
                    
                    # Save model
                    model.save("model/health_model.keras")
                    
                    # Save preprocessors
                    joblib.dump(env_scaler, "model/env_scaler.joblib")
                    joblib.dump(wearable_scaler, "model/wearable_scaler.joblib")
                    joblib.dump(text_encoder, "model/text_encoder.joblib")
                    
                    print("Model saved to model/health_model.keras")
                    print("Preprocessors saved to model/ directory")
                    print("=" * 60)
                except Exception as e:
                    print(f"  Warning: Could not save model: {e}")
                    import traceback
                    traceback.print_exc()
            
            return aggregated
    
    strategy = FedAvgWithSave(
        min_fit_clients=args.min_clients,  # Wait for minimum clients to train
        min_evaluate_clients=args.min_clients,  # Evaluate on minimum clients
        min_available_clients=args.min_clients,  # Wait for minimum clients to be available
    )

    # Start the server
    try:
        fl.server.start_server(
            server_address=f"0.0.0.0:{args.port}",
            config=fl.server.ServerConfig(num_rounds=args.rounds),
            strategy=strategy,
        )
        print("\n" + "=" * 60)
        print("Federated Learning completed successfully!")
        print("=" * 60)
    except KeyboardInterrupt:
        print("\n\nServer stopped by user.")
        sys.exit(0)
    except Exception as e:
        print(f"\n\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

