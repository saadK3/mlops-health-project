"""
Federated Learning Client
Runs on each hospital/city machine and participates in federated learning.
"""
import flwr as fl
import argparse
import sys
import os

# Import shared components from train.py
from train import HealthRiskClient, CLIENT_CITIES, DATA_FILE_PATH

def main():
    parser = argparse.ArgumentParser(
        description="Federated Learning Client for Health Risk Prediction"
    )
    parser.add_argument(
        "--city",
        type=str,
        required=True,
        choices=CLIENT_CITIES,
        help=f"City name for this client. Options: {', '.join(CLIENT_CITIES)}",
    )
    parser.add_argument(
        "--server",
        type=str,
        default="localhost:9090",
        help="Server address in format 'host:port' (default: localhost:9090)",
    )
    args = parser.parse_args()

    # Validate data file exists
    if not os.path.exists(DATA_FILE_PATH):
        print(f"ERROR: Data file not found at {DATA_FILE_PATH}")
        print("Please ensure the data file exists before running the client.")
        sys.exit(1)

    print("=" * 60)
    print(f"Federated Learning Client: {args.city}")
    print("=" * 60)
    print(f"Connecting to server: {args.server}")
    print(f"Local data file: {DATA_FILE_PATH}")
    print("=" * 60)
    print()

    # Create client instance
    try:
        client = HealthRiskClient(client_city=args.city)
        
        print(f"Connecting {args.city} client to server at {args.server}...")
        print("This may take a moment if the server is not yet ready.\n")
        
        # Connect to server and participate in federated learning
        fl.client.start_numpy_client(
            server_address=args.server,
            client=client,
        )
        
        print("\n" + "=" * 60)
        print(f"{args.city} client finished successfully!")
        print("=" * 60)
        
    except KeyboardInterrupt:
        print(f"\n\n{args.city} client stopped by user.")
        sys.exit(0)
    except ConnectionRefusedError:
        print(f"\n\nERROR: Could not connect to server at {args.server}")
        print("Please ensure the server is running and the address is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\nERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    main()

