"""
MLflow Experiment Viewer
Script to view and query MLflow experiments and runs.
"""
import mlflow
from mlflow.tracking import MlflowClient
import pandas as pd
from datetime import datetime

def list_experiments():
    """List all experiments."""
    client = MlflowClient()
    experiments = client.search_experiments()
    
    print("=" * 80)
    print("MLflow Experiments")
    print("=" * 80)
    
    if not experiments:
        print("No experiments found.")
        return
    
    for exp in experiments:
        print(f"\n📊 Experiment: {exp.name}")
        print(f"   ID: {exp.experiment_id}")
        print(f"   Artifact Location: {exp.artifact_location}")
        print(f"   Lifecycle Stage: {exp.lifecycle_stage}")
        
        # Get runs for this experiment
        runs = client.search_runs(experiment_ids=[exp.experiment_id], max_results=5)
        print(f"   Recent Runs: {len(runs)}")
        
        if runs:
            print("   Latest runs:")
            for i, run in enumerate(runs[:3], 1):
                print(f"      {i}. {run.info.run_name}")
                print(f"         Run ID: {run.info.run_id}")
                print(f"         Status: {run.info.status}")
                print(f"         Start Time: {datetime.fromtimestamp(run.info.start_time/1000)}")
                if run.data.metrics:
                    print(f"         Metrics: {list(run.data.metrics.keys())[:3]}...")
    
    print("\n" + "=" * 80)


def view_experiment_details(experiment_name):
    """View detailed information about a specific experiment."""
    client = MlflowClient()
    
    try:
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment is None:
            print(f"❌ Experiment '{experiment_name}' not found.")
            return
        
        print("=" * 80)
        print(f"Experiment: {experiment_name}")
        print("=" * 80)
        
        # Get all runs
        runs = client.search_runs(experiment_ids=[experiment.experiment_id])
        
        print(f"\nTotal Runs: {len(runs)}")
        
        if not runs:
            print("No runs found in this experiment.")
            return
        
        # Create a summary DataFrame
        run_data = []
        for run in runs:
            run_info = {
                "Run ID": run.info.run_id[:8] + "...",
                "Run Name": run.info.run_name,
                "Status": run.info.status,
                "Start Time": datetime.fromtimestamp(run.info.start_time/1000).strftime("%Y-%m-%d %H:%M:%S"),
            }
            
            # Add key metrics
            if run.data.metrics:
                for key in ["final_test_mae", "final_test_rmse", "final_test_r2", "overall_mae", "overall_r2"]:
                    if key in run.data.metrics:
                        run_info[key] = f"{run.data.metrics[key]:.4f}"
            
            # Add key parameters
            if run.data.params:
                for key in ["training_method", "epochs", "num_clients"]:
                    if key in run.data.params:
                        run_info[key] = run.data.params[key]
            
            run_data.append(run_info)
        
        df = pd.DataFrame(run_data)
        print("\n" + df.to_string(index=False))
        
        # Show best run
        if runs:
            best_run = min(runs, key=lambda r: r.data.metrics.get("final_test_mae", float('inf')) if r.data.metrics else float('inf'))
            if best_run.data.metrics:
                print("\n" + "=" * 80)
                print("🏆 Best Run (Lowest MAE):")
                print("=" * 80)
                print(f"   Run Name: {best_run.info.run_name}")
                print(f"   Run ID: {best_run.info.run_id}")
                print(f"   Metrics:")
                for key, value in best_run.data.metrics.items():
                    print(f"      {key}: {value:.4f}")
                print(f"   Parameters:")
                for key, value in best_run.data.params.items():
                    print(f"      {key}: {value}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def compare_runs(experiment_name, metric="final_test_mae"):
    """Compare runs in an experiment by a specific metric."""
    client = MlflowClient()
    
    try:
        experiment = client.get_experiment_by_name(experiment_name)
        if experiment is None:
            print(f"❌ Experiment '{experiment_name}' not found.")
            return
        
        runs = client.search_runs(experiment_ids=[experiment.experiment_id])
        
        if not runs:
            print("No runs found.")
            return
        
        print("=" * 80)
        print(f"Comparing Runs by {metric}")
        print("=" * 80)
        
        # Filter runs that have this metric
        valid_runs = [r for r in runs if r.data.metrics and metric in r.data.metrics]
        
        if not valid_runs:
            print(f"No runs have the metric '{metric}'.")
            return
        
        # Sort by metric
        valid_runs.sort(key=lambda r: r.data.metrics[metric])
        
        print(f"\n{'Rank':<6} {'Run Name':<30} {metric:<15} {'Status':<10}")
        print("-" * 80)
        
        for i, run in enumerate(valid_runs[:10], 1):
            metric_value = run.data.metrics[metric]
            print(f"{i:<6} {run.info.run_name[:30]:<30} {metric_value:<15.4f} {run.info.status:<10}")
        
    except Exception as e:
        print(f"❌ Error: {e}")


def main():
    """Main menu."""
    print("\n" + "=" * 80)
    print("MLflow Experiment Viewer")
    print("=" * 80)
    print("\nOptions:")
    print("1. List all experiments")
    print("2. View experiment details")
    print("3. Compare runs by metric")
    print("4. Exit")
    
    choice = input("\nEnter your choice (1-4): ").strip()
    
    if choice == "1":
        list_experiments()
    elif choice == "2":
        exp_name = input("Enter experiment name (e.g., 'health-risk-prediction'): ").strip()
        view_experiment_details(exp_name)
    elif choice == "3":
        exp_name = input("Enter experiment name: ").strip()
        metric = input("Enter metric name (e.g., 'final_test_mae'): ").strip() or "final_test_mae"
        compare_runs(exp_name, metric)
    elif choice == "4":
        print("Goodbye!")
    else:
        print("Invalid choice.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nExiting...")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

