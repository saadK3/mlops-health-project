"""
Automated Distributed Federated Learning Launcher
Runs server and all clients automatically with detailed progress tracking.
"""
import subprocess
import threading
import time
import sys
import os
import signal
from queue import Queue
from train import (
    CLIENT_CITIES,
    build_multi_modal_model,
    HealthRiskClient,
    initialize_preprocessors,
    env_scaler,
    wearable_scaler,
    text_encoder,
    DATA_FILE_PATH,
)
import joblib

# Configuration
SERVER_PORT = 9090
NUM_ROUNDS = 3
SERVER_ADDRESS = f"localhost:{SERVER_PORT}"

# Global process list for cleanup
processes = []


def print_colored(text, color="white"):
    """Print colored text (simple version, works on most terminals)."""
    colors = {
        "red": "\033[91m",
        "green": "\033[92m",
        "yellow": "\033[93m",
        "blue": "\033[94m",
        "magenta": "\033[95m",
        "cyan": "\033[96m",
        "white": "\033[97m",
        "reset": "\033[0m",
    }
    print(f"{colors.get(color, '')}{text}{colors['reset']}")


def read_output(pipe, queue, label, color):
    """Read output from a process and put it in a queue with label."""
    try:
        for line in iter(pipe.readline, b''):
            if line:
                queue.put((label, color, line.decode('utf-8', errors='ignore').rstrip()))
        pipe.close()
    except Exception as e:
        queue.put((label, color, f"Error reading output: {e}"))


def start_server(port, rounds):
    """Start the FL server in a subprocess."""
    cmd = [sys.executable, "server.py", "--port", str(port), "--rounds", str(rounds)]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=False
    )
    return process


def start_client(city, server_address):
    """Start an FL client in a subprocess."""
    cmd = [sys.executable, "client.py", "--city", city, "--server", server_address]
    process = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        bufsize=1,
        universal_newlines=False
    )
    return process


def display_output(queue, stop_event):
    """Display output from all processes with labels."""
    while not stop_event.is_set() or not queue.empty():
        try:
            label, color, line = queue.get(timeout=0.1)
            if line.strip():
                print_colored(f"[{label}] {line}", color)
        except:
            continue


def cleanup_processes():
    """Clean up all processes on exit."""
    print_colored("\n\n🛑 Shutting down all processes...", "yellow")
    for process in processes:
        try:
            process.terminate()
            process.wait(timeout=5)
        except:
            try:
                process.kill()
            except:
                pass
    print_colored("✅ All processes terminated.", "green")


def signal_handler(sig, frame):
    """Handle Ctrl+C gracefully."""
    cleanup_processes()
    sys.exit(0)


def verify_model_saved():
    """Verify that the model was saved by the server."""
    print_colored("\n" + "=" * 70, "cyan")
    print_colored("🔍 Verifying Model Save...", "cyan")
    print_colored("=" * 70, "cyan")
    
    model_path = "model/health_model.keras"
    required_files = [
        "model/health_model.keras",
        "model/env_scaler.joblib",
        "model/wearable_scaler.joblib",
        "model/text_encoder.joblib",
    ]
    
    all_exist = True
    for file_path in required_files:
        if os.path.exists(file_path):
            print_colored(f"   ✅ {file_path}", "green")
        else:
            print_colored(f"   ❌ {file_path} (missing)", "red")
            all_exist = False
    
    if all_exist:
        print_colored("\n" + "=" * 70, "green")
        print_colored("✅ All model files verified!", "green")
        print_colored("=" * 70, "green")
        return True
    else:
        print_colored("\n" + "=" * 70, "yellow")
        print_colored("⚠️  Some model files are missing.", "yellow")
        print_colored("The server should have saved them automatically.", "yellow")
        print_colored("=" * 70, "yellow")
        return False


def main():
    """Main launcher function."""
    # Register signal handler for graceful shutdown
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Check if data file exists
    from train import DATA_FILE_PATH
    if not os.path.exists(DATA_FILE_PATH):
        print_colored(f"❌ ERROR: Data file not found at {DATA_FILE_PATH}", "red")
        print_colored("Please ensure the data file exists before running.", "red")
        sys.exit(1)
    
    print_colored("=" * 70, "cyan")
    print_colored("🚀 Automated Distributed Federated Learning Launcher", "cyan")
    print_colored("=" * 70, "cyan")
    print_colored(f"📊 Cities: {', '.join(CLIENT_CITIES)}", "white")
    print_colored(f"🔄 Rounds: {NUM_ROUNDS}", "white")
    print_colored(f"🌐 Port: {SERVER_PORT}", "white")
    print_colored("=" * 70, "cyan")
    print()
    
    # Queue for output from all processes
    output_queue = Queue()
    stop_event = threading.Event()
    
    # Start output display thread
    display_thread = threading.Thread(
        target=display_output,
        args=(output_queue, stop_event),
        daemon=True
    )
    display_thread.start()
    
    # Step 1: Start server
    print_colored("📡 Starting FL Server...", "blue")
    server_process = start_server(SERVER_PORT, NUM_ROUNDS)
    processes.append(server_process)
    
    # Start reading server output
    server_thread = threading.Thread(
        target=read_output,
        args=(server_process.stdout, output_queue, "SERVER", "blue"),
        daemon=True
    )
    server_thread.start()
    
    # Wait for server to start
    print_colored("⏳ Waiting for server to initialize (3 seconds)...", "yellow")
    time.sleep(3)
    
    # Step 2: Start all clients
    print_colored(f"👥 Starting {len(CLIENT_CITIES)} clients...", "green")
    client_colors = ["green", "magenta", "yellow", "cyan"]
    
    for i, city in enumerate(CLIENT_CITIES):
        print_colored(f"   → Starting client: {city}", "white")
        client_process = start_client(city, SERVER_ADDRESS)
        processes.append(client_process)
        
        # Start reading client output
        color = client_colors[i % len(client_colors)]
        client_thread = threading.Thread(
            target=read_output,
            args=(client_process.stdout, output_queue, city.upper(), color),
            daemon=True
        )
        client_thread.start()
        
        # Small delay between client starts
        time.sleep(0.5)
    
    print_colored("\n" + "=" * 70, "cyan")
    print_colored("✅ All processes started! Training in progress...", "green")
    print_colored("=" * 70, "cyan")
    print_colored("💡 Press Ctrl+C to stop all processes\n", "yellow")
    print()
    
    # Wait for all processes to complete
    try:
        # Wait for server to finish (it will finish last)
        server_process.wait()
        
        # Wait a bit for clients to finish
        time.sleep(2)
        
        # Check if all clients are done
        for i, process in enumerate(processes[1:], 1):  # Skip server (index 0)
            if process.poll() is None:  # Still running
                process.wait(timeout=30)
        
        stop_event.set()
        time.sleep(1)  # Let display thread finish
        
        print_colored("\n" + "=" * 70, "green")
        print_colored("🎉 Federated Learning Completed Successfully!", "green")
        print_colored("=" * 70, "green")
        
        # Step 3: Verify model was saved (server saves it automatically)
        # Wait a moment for server to finish saving
        time.sleep(1)
        model_saved = verify_model_saved()
        
        if model_saved:
            print_colored("\n" + "=" * 70, "green")
            print_colored("✨ All Done! Ready for deployment.", "green")
            print_colored("=" * 70, "green")
            print_colored("\n📝 Next steps:", "cyan")
            print_colored("   1. Test the API: python app.py", "white")
            print_colored("   2. Check data drift: python data_drift.py", "white")
            print_colored("   3. Deploy: docker build -t health-api .", "white")
            print_colored("=" * 70, "cyan")
        else:
            print_colored("\n⚠️  Model files verification failed.", "yellow")
            print_colored("The server should have saved the model automatically.", "yellow")
            print_colored("Check server logs for any errors.", "yellow")
        
    except KeyboardInterrupt:
        print_colored("\n\n⚠️  Interrupted by user", "yellow")
        cleanup_processes()
    except Exception as e:
        print_colored(f"\n\n❌ Error: {e}", "red")
        cleanup_processes()
        sys.exit(1)


if __name__ == "__main__":
    main()

