import pandas as pd
from scipy.stats import ks_2samp
import warnings

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

print("--- Data Drift Detection Script ---")

# --- 1. Configuration ---
DATA_FILE_PATH = 'C:/Users/This Pc/Documents/mlops/mlops-health-project/data/MLOPs_data.csv'
# We will check for drift on our most important features
FEATURES_TO_CHECK = ['pm2_5', 'occupancy_ratio', 'heart_rate', 'respiratory_rate']
# Our p-value threshold. If p < 0.05, we say it's drifted.
P_VALUE_THRESHOLD = 0.05

# --- 2. Load and Prepare Data ---
try:
    df = pd.read_csv(DATA_FILE_PATH, encoding='latin1')
    print(f"Loaded data successfully. Total rows: {len(df)}")
except Exception as e:
    print(f"Error loading data: {e}")
    exit()

# Define our "reference" (training) and "new" (live) data
# For this simulation, we'll use the first 80% as reference
# and the last 20% as "new" data to make the test meaningful.
n_rows = len(df)
n_reference = int(n_rows * 0.8)
n_new = n_rows - n_reference

df_reference = df.head(n_reference)
df_new = df.tail(n_new)

print(f"Reference data size:",df_reference)
print(f"Reference data size: {len(df_reference)} rows")

print(f"New data size: {len(df_new)} rows\n")

# --- 3. Run Drift Detection ---
print("--- Running Drift Tests ---")
drift_detected = False

for feature in FEATURES_TO_CHECK:
    # Get the data for the feature from both dataframes
    reference_data = df_reference[feature]
    new_data = df_new[feature]
    
    # Perform the Kolmogorov-Smirnov test
    # This test compares two distributions
    ks_statistic, p_value = ks_2samp(reference_data, new_data)
    
    print(f"Feature: '{feature}'")
    print(f"  KS Statistic: {ks_statistic:.4f}")
    print(f"  P-Value: {p_value:.4f}")
    
    # --- 4. Report Findings ---
    if p_value < P_VALUE_THRESHOLD:
        print(f"  ALARM: Data drift detected! (p-value {p_value:.4f} < {P_VALUE_THRESHOLD})")
        drift_detected = True
    else:
        print(f"  OK: No significant drift detected. (p-value {p_value:.4f} >= {P_VALUE_THRESHOLD})")
    print("-" * 20)

print("\n--- Summary ---")
if drift_detected:
    print(" At least one feature has drifted. Model retraining may be necessary.")
else:
    print(" All checked features are stable. No drift detected.")