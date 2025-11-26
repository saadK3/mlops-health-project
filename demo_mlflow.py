"""
Quick demo script to show MLflow experiment tracking in action.
Run this to see how MLflow tracks experiments.
"""
import mlflow
import mlflow.keras
import numpy as np
from datetime import datetime
import os

# Set experiment
mlflow.set_experiment("mlflow-demo")

print("=" * 60)
print("MLflow Demo - Experiment Tracking")
print("=" * 60)

# Start a demo run
with mlflow.start_run(run_name=f"demo_run_{datetime.now().strftime('%Y%m%d_%H%M%S')}"):
    print("\n📊 Starting MLflow run...")
    
    # Log some parameters
    print("   Logging parameters...")
    mlflow.log_param("demo_type", "example")
    mlflow.log_param("random_seed", 42)
    mlflow.log_param("sample_size", 1000)
    
    # Simulate some metrics (like training)
    print("   Logging metrics...")
    for epoch in range(5):
        # Simulate training metrics
        train_loss = 10.0 - (epoch * 1.5) + np.random.normal(0, 0.2)
        val_loss = 10.5 - (epoch * 1.4) + np.random.normal(0, 0.3)
        
        mlflow.log_metric("train_loss", train_loss, step=epoch)
        mlflow.log_metric("val_loss", val_loss, step=epoch)
        print(f"      Epoch {epoch+1}: train_loss={train_loss:.3f}, val_loss={val_loss:.3f}")
    
    # Log final metrics
    final_mae = 2.5 + np.random.normal(0, 0.1)
    final_r2 = 0.85 + np.random.normal(0, 0.02)
    
    mlflow.log_metric("final_mae", final_mae)
    mlflow.log_metric("final_r2", final_r2)
    
    print(f"\n   Final Metrics:")
    print(f"      MAE: {final_mae:.4f}")
    print(f"      R²: {final_r2:.4f}")
    
    # Log an artifact (example)
    print("\n   Logging artifacts...")
    demo_file = "demo_artifact.txt"
    with open(demo_file, "w") as f:
        f.write("This is a demo artifact for MLflow tracking.\n")
        f.write(f"Created at: {datetime.now()}\n")
        f.write(f"Final MAE: {final_mae:.4f}\n")
    
    mlflow.log_artifact(demo_file, "demo_artifacts")
    os.remove(demo_file)  # Clean up
    
    print("   ✅ Artifact logged")
    
    # Get run info
    run_id = mlflow.active_run().info.run_id
    print(f"\n✅ Run completed!")
    print(f"   Run ID: {run_id}")
    print(f"   Experiment: mlflow-demo")
    
print("\n" + "=" * 60)
print("📊 View your experiment:")
print("   1. Run: mlflow ui")
print("   2. Open: http://localhost:5000")
print("   3. Click on 'mlflow-demo' experiment")
print("=" * 60)

