# MLflow Integration Summary

## ✅ What Has Been Integrated

MLflow experiment tracking has been fully integrated into the MLOps Health Risk Prediction project.

### 1. Training Scripts (`train_simple.py` & `train.py`)

**Location:** `train_simple.py` (lines 144-242)

**What's Tracked:**
- ✅ Training hyperparameters (epochs, batch_size, learning_rate)
- ✅ Data information (train/test samples, feature counts)
- ✅ Training metrics per epoch (loss, MAE for train/val)
- ✅ Final evaluation metrics (MSE, MAE, RMSE, R²)
- ✅ Model artifacts (saved model, preprocessors)
- ✅ Model registration in MLflow

**Experiment:** `health-risk-prediction`

### 2. Model Evaluation (`test_model_performance.py`)

**Location:** `test_model_performance.py` (updated main function)

**What's Tracked:**
- ✅ Overall performance metrics (MSE, MAE, RMSE, R²)
- ✅ Per-city performance metrics
- ✅ Test sample counts
- ✅ API endpoint test results

**Experiment:** `model-evaluation`

### 3. Production API (`app.py`)

**Location:** `app.py` (predict endpoint, lines 150-186)

**What's Tracked:**
- ✅ Prediction values (10% sampling to avoid overload)
- ✅ Response times
- ✅ Input parameters (population_density, AQI)

**Experiment:** `production-inference`

### 4. Utility Scripts

**Created Files:**
- ✅ `view_mlflow_experiments.py` - Command-line tool to view experiments
- ✅ `demo_mlflow.py` - Demo script showing MLflow in action
- ✅ `MLFLOW_GUIDE.md` - Comprehensive usage guide

## How to Use

### Step 1: Install MLflow (if not already installed)

```bash
.\venv\Scripts\Activate.ps1
pip install mlflow
```

### Step 2: Run Training (automatically tracks to MLflow)

```bash
python train_simple.py
```

You'll see output like:
```
📊 MLflow Run Info:
   Experiment: health-risk-prediction
   Run ID: abc123def456...
   View UI: mlflow ui (then open http://localhost:5000)
```

### Step 3: View Experiments

**Option A: MLflow UI (Recommended)**

```bash
mlflow ui
```

Then open: **http://localhost:5000**

**Option B: Command Line**

```bash
python view_mlflow_experiments.py
```

### Step 4: Run Evaluation (tracks to MLflow)

```bash
python test_model_performance.py
```

This creates a new run in the `model-evaluation` experiment.

### Step 5: Production Tracking

When you run the Flask API:

```bash
python app.py
```

Every 10th prediction request is automatically logged to MLflow in the `production-inference` experiment.

## What You Can Do with MLflow

### 1. Compare Training Runs

- View all training runs side-by-side
- Compare metrics (MAE, RMSE, R²)
- See which hyperparameters work best
- Download the best model

### 2. Track Model Performance Over Time

- See how model performance changes with different training runs
- Identify when model quality degrades
- Track evaluation metrics across different test sets

### 3. Monitor Production

- Track prediction values in real-time
- Monitor API response times
- Detect anomalies in predictions

### 4. Reproduce Experiments

- All parameters are logged
- Can reproduce any training run
- Model artifacts are stored

## Experiments Structure

```
mlruns/
├── 0/  (health-risk-prediction)
│   ├── runs/
│   │   ├── run_1/  (training run 1)
│   │   ├── run_2/  (training run 2)
│   │   └── ...
│
├── 1/  (model-evaluation)
│   ├── runs/
│   │   ├── run_1/  (evaluation run 1)
│   │   └── ...
│
└── 2/  (production-inference)
    ├── runs/
    │   ├── run_1/  (inference sample 1)
    │   └── ...
```

## Key Features

### ✅ Automatic Tracking
- No manual logging needed
- Integrated into existing scripts
- Works automatically when scripts run

### ✅ Comprehensive Metrics
- Training metrics (per epoch)
- Evaluation metrics (overall + per-city)
- Production metrics (sampled)

### ✅ Model Artifacts
- Models saved to MLflow
- Preprocessors logged
- Easy model retrieval

### ✅ Experiment Organization
- Separate experiments for training/evaluation/production
- Easy to filter and compare
- Clear run names with timestamps

## Example Workflow

1. **Train a model:**
   ```bash
   python train_simple.py
   ```
   → Creates run in `health-risk-prediction` experiment

2. **Evaluate the model:**
   ```bash
   python test_model_performance.py
   ```
   → Creates run in `model-evaluation` experiment

3. **View results:**
   ```bash
   mlflow ui
   ```
   → Compare training vs evaluation metrics

4. **Deploy and monitor:**
   ```bash
   python app.py
   ```
   → Production predictions tracked in `production-inference`

## Integration Points

| Component | MLflow Integration | Status |
|-----------|-------------------|--------|
| `train_simple.py` | Full tracking | ✅ Complete |
| `train.py` | Full tracking | ✅ Complete |
| `test_model_performance.py` | Evaluation tracking | ✅ Complete |
| `app.py` | Production tracking | ✅ Complete |
| CI/CD Pipeline | Can be enhanced | ⚠️ Optional |

## Next Steps (Optional Enhancements)

1. **Model Registry**: Set up MLflow Model Registry for versioning
2. **CI/CD Integration**: Auto-compare models in CI/CD pipeline
3. **Cloud Storage**: Use S3/Azure Blob for artifact storage
4. **Automated Alerts**: Alert when model performance degrades
5. **A/B Testing**: Track different model versions in production

## Troubleshooting

**MLflow not found:**
```bash
pip install mlflow
```

**Port 5000 already in use:**
```bash
mlflow ui --port 5001
```

**Experiments not showing:**
- Check that scripts ran successfully
- Verify `mlruns/` directory exists
- Check experiment names match

## Summary

✅ **MLflow is fully integrated** across:
- Training scripts
- Evaluation scripts  
- Production API
- Utility tools

✅ **Ready to use** - just run your scripts and view in MLflow UI!

✅ **Comprehensive tracking** - parameters, metrics, artifacts all logged

✅ **Easy to use** - automatic tracking, no manual intervention needed

