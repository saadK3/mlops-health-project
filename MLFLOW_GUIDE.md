# MLflow Experiment Tracking Guide

This guide explains how to use MLflow for experiment tracking in the MLOps Health Risk Prediction project.

## Overview

MLflow is integrated throughout the project to track:
- **Training experiments** - Model training runs with hyperparameters and metrics
- **Model evaluation** - Performance metrics on test data
- **Production inference** - Real-time prediction tracking (sampled)

## Setup

MLflow is already installed in `requirements.txt`. No additional setup needed!

## Experiments

The project uses three main MLflow experiments:

1. **`health-risk-prediction`** - Training experiments
   - Tracks model training runs
   - Logs hyperparameters, metrics, and model artifacts
   - Used by `train_simple.py` and `train.py`

2. **`model-evaluation`** - Model evaluation runs
   - Tracks evaluation metrics on test data
   - Logs per-city and overall performance
   - Used by `test_model_performance.py`

3. **`production-inference`** - Production prediction tracking
   - Tracks inference requests (10% sampling)
   - Logs prediction values and response times
   - Used by `app.py` (Flask API)

## Usage

### 1. View MLflow UI

Start the MLflow UI to view experiments in a web interface:

```bash
# Activate virtual environment
.\venv\Scripts\Activate.ps1

# Start MLflow UI
mlflow ui
```

Then open your browser to: **http://localhost:5000**

The UI shows:
- All experiments
- Runs with parameters and metrics
- Model artifacts
- Comparison between runs

### 2. View Experiments via Script

Use the provided script to view experiments from command line:

```bash
python view_mlflow_experiments.py
```

Options:
1. List all experiments
2. View experiment details
3. Compare runs by metric
4. Exit

### 3. Training with MLflow Tracking

When you run training, MLflow automatically tracks:

```bash
python train_simple.py
```

This logs:
- **Parameters**: epochs, batch_size, learning_rate, feature counts, etc.
- **Metrics**: Training/validation loss and MAE per epoch, final test metrics
- **Artifacts**: Model file, preprocessors
- **Model**: Registered model in MLflow

### 4. Evaluation with MLflow Tracking

Run model evaluation:

```bash
python test_model_performance.py
```

This logs:
- **Metrics**: Overall and per-city MSE, MAE, RMSE, R²
- **Parameters**: Model type, test sample counts
- **API Test Results**: API endpoint validation

### 5. Production Tracking

The Flask API (`app.py`) automatically tracks:
- Prediction values (sampled 10% of requests)
- Response times
- Input parameters (population_density, AQI)

## What Gets Tracked

### Training Runs (`train_simple.py`)

**Parameters:**
- `training_method`: "simple_direct"
- `epochs`: Number of training epochs
- `batch_size`: Training batch size
- `learning_rate`: Learning rate
- `train_samples`: Number of training samples
- `test_samples`: Number of test samples
- `env_features_count`: Number of environmental features
- `wearable_features_count`: Number of wearable features
- `test_split`: Test data split ratio
- `random_seed`: Random seed for reproducibility

**Metrics (per epoch):**
- `train_loss`: Training loss
- `val_loss`: Validation loss
- `train_mae`: Training MAE
- `val_mae`: Validation MAE

**Final Metrics:**
- `final_test_loss`: Final test loss
- `final_test_mae`: Final test MAE
- `final_test_mse`: Final test MSE
- `final_test_rmse`: Final test RMSE
- `final_test_r2`: Final test R²

**Artifacts:**
- Model file (`model/health_model.keras`)
- Preprocessors (`env_scaler.joblib`, `wearable_scaler.joblib`, `text_encoder.joblib`)

### Evaluation Runs (`test_model_performance.py`)

**Metrics:**
- `overall_mse`, `overall_mae`, `overall_rmse`, `overall_r2`
- Per-city metrics: `{city}_mse`, `{city}_mae`, `{city}_rmse`, `{city}_r2`

**Parameters:**
- `model_type`: "multi_modal_health_risk"
- `total_test_samples`: Total test samples
- Per-city sample counts: `{city}_samples`

### Production Runs (`app.py`)

**Metrics (sampled 10%):**
- `prediction_value`: Predicted hospital admissions
- `response_time_ms`: API response time in milliseconds

**Parameters:**
- `population_density`: Input population density
- `aqi`: Input AQI value

## Querying Experiments

### Using MLflow Python API

```python
import mlflow
from mlflow.tracking import MlflowClient

client = MlflowClient()

# Get experiment
experiment = client.get_experiment_by_name("health-risk-prediction")

# Get runs
runs = client.search_runs(experiment_ids=[experiment.experiment_id])

# Get best run
best_run = min(runs, key=lambda r: r.data.metrics.get("final_test_mae", float('inf')))
print(f"Best MAE: {best_run.data.metrics['final_test_mae']}")
```

### Using MLflow UI

1. Start UI: `mlflow ui`
2. Open http://localhost:5000
3. Click on an experiment
4. Compare runs side-by-side
5. View metrics over time
6. Download model artifacts

## Best Practices

1. **Run Names**: Use descriptive run names with timestamps
   - Example: `train_simple_20241123_143022`

2. **Parameter Logging**: Log all hyperparameters that affect model performance

3. **Metric Logging**: Log metrics at each epoch for training curves

4. **Artifact Logging**: Always log model files and preprocessors

5. **Experiment Organization**: Use separate experiments for:
   - Training
   - Evaluation
   - Production

## CI/CD Integration

The CI/CD pipeline (`.github/workflows/ci-cd-pipeline.yaml`) can be enhanced to:
- Track training runs in CI
- Compare model versions
- Automatically register best models

## Troubleshooting

### MLflow UI not starting
- Check if port 5000 is already in use
- Use `mlflow ui --port 5001` to use a different port

### Experiments not showing
- Check that MLflow tracking URI is set correctly
- Default: `./mlruns` directory (local file system)

### Too many production runs
- Production tracking uses 10% sampling to avoid overwhelming MLflow
- Adjust sampling rate in `app.py` if needed

## Example Workflow

1. **Train a model:**
   ```bash
   python train_simple.py
   ```
   - Model is logged to MLflow
   - Run ID is printed

2. **Evaluate the model:**
   ```bash
   python test_model_performance.py
   ```
   - Evaluation metrics logged
   - Can compare with training metrics

3. **View results:**
   ```bash
   mlflow ui
   ```
   - Open http://localhost:5000
   - Compare training vs evaluation
   - Download best model

4. **Deploy best model:**
   - Use MLflow to load the best model
   - Deploy to production
   - Monitor via production-inference experiment

## Next Steps

- Set up MLflow Model Registry for model versioning
- Integrate with cloud storage (S3, Azure Blob) for artifact storage
- Add automated model comparison in CI/CD
- Set up alerts for model performance degradation

