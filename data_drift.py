"""
Data Drift Detection Script
Compares training data (reference) against test/production data to detect distribution changes.
"""
import pandas as pd
import numpy as np
from scipy.stats import ks_2samp, chi2_contingency
import joblib
import os
import warnings
from sklearn.model_selection import train_test_split

# Import feature definitions from train.py to ensure consistency
from train import (
    DATA_FILE_PATH,
    ENV_FEATURES,
    WEARABLE_FEATURES,
    TEXT_FEATURE,
    TARGET,
    CLIENT_CITIES,
)

# Suppress warnings for cleaner output
warnings.filterwarnings('ignore')

# Configuration
P_VALUE_THRESHOLD = 0.05
REFERENCE_STATS_FILE = "model/reference_stats.joblib"


def calculate_reference_statistics(df_train):
    """
    Calculate reference statistics from training data.
    Returns a dictionary with statistics for each feature.
    """
    stats = {}
    
    # Numerical features (ENV + WEARABLE)
    all_numerical_features = ENV_FEATURES + WEARABLE_FEATURES
    
    for feature in all_numerical_features:
        if feature in df_train.columns:
            stats[feature] = {
                'mean': float(df_train[feature].mean()),
                'std': float(df_train[feature].std()),
                'min': float(df_train[feature].min()),
                'max': float(df_train[feature].max()),
                'median': float(df_train[feature].median()),
                'data': df_train[feature].values.tolist()  # For KS test
            }
    
    # Categorical feature (TEXT_FEATURE)
    if TEXT_FEATURE in df_train.columns:
        stats[TEXT_FEATURE] = {
            'value_counts': df_train[TEXT_FEATURE].value_counts().to_dict()
        }
    
    return stats


def save_reference_statistics(stats, filepath=REFERENCE_STATS_FILE):
    """Save reference statistics to a file."""
    os.makedirs(os.path.dirname(filepath) if os.path.dirname(filepath) else '.', exist_ok=True)
    joblib.dump(stats, filepath)
    print(f"✅ Reference statistics saved to {filepath}")


def load_reference_statistics(filepath=REFERENCE_STATS_FILE):
    """Load reference statistics from a file."""
    if not os.path.exists(filepath):
        return None
    return joblib.load(filepath)


def detect_numerical_drift(reference_data, new_data, feature_name):
    """
    Detect drift in numerical features using Kolmogorov-Smirnov test.
    Returns (drifted, ks_statistic, p_value, summary_stats)
    """
    ks_statistic, p_value = ks_2samp(reference_data, new_data)
    
    ref_mean = np.mean(reference_data)
    ref_std = np.std(reference_data)
    new_mean = np.mean(new_data)
    new_std = np.std(new_data)
    
    mean_shift = abs(new_mean - ref_mean) / (ref_std + 1e-8)  # Normalized shift
    std_shift = abs(new_std - ref_std) / (ref_std + 1e-8)
    
    drifted = p_value < P_VALUE_THRESHOLD
    
    summary = {
        'drifted': drifted,
        'ks_statistic': float(ks_statistic),
        'p_value': float(p_value),
        'ref_mean': float(ref_mean),
        'ref_std': float(ref_std),
        'new_mean': float(new_mean),
        'new_std': float(new_std),
        'mean_shift': float(mean_shift),
        'std_shift': float(std_shift),
    }
    
    return drifted, summary


def detect_categorical_drift(reference_counts, new_data, feature_name):
    """
    Detect drift in categorical features using Chi-square test.
    Returns (drifted, chi2_statistic, p_value, summary_stats)
    """
    # Get value counts for new data
    new_counts = pd.Series(new_data).value_counts().to_dict()
    
    # Create contingency table
    all_categories = set(reference_counts.keys()) | set(new_counts.keys())
    
    # Build contingency table
    ref_values = [reference_counts.get(cat, 0) for cat in all_categories]
    new_values = [new_counts.get(cat, 0) for cat in all_categories]
    
    contingency = np.array([ref_values, new_values])
    
    # Perform chi-square test
    try:
        chi2, p_value, dof, expected = chi2_contingency(contingency)
        drifted = p_value < P_VALUE_THRESHOLD
        
        summary = {
            'drifted': drifted,
            'chi2_statistic': float(chi2),
            'p_value': float(p_value),
            'reference_distribution': reference_counts,
            'new_distribution': new_counts,
        }
        
        return drifted, summary
    except Exception as e:
        print(f"  ⚠️  Warning: Could not perform chi-square test: {e}")
        return False, {'error': str(e)}


def run_drift_detection(df_reference, df_new, reference_stats=None):
    """
    Run drift detection comparing reference (training) data against new (test/production) data.
    """
    print("=" * 60)
    print("Running Drift Detection")
    print("=" * 60)
    
    drift_results = {}
    any_drift = False
    
    # Check numerical features
    all_numerical_features = ENV_FEATURES + WEARABLE_FEATURES
    
    print(f"\n📊 Checking {len(all_numerical_features)} numerical features...")
    print("-" * 60)
    
    for feature in all_numerical_features:
        if feature not in df_reference.columns or feature not in df_new.columns:
            print(f"⚠️  Feature '{feature}' not found in data, skipping...")
            continue
        
        reference_data = df_reference[feature].dropna()
        new_data = df_new[feature].dropna()
        
        if len(reference_data) == 0 or len(new_data) == 0:
            print(f"⚠️  Feature '{feature}' has no valid data, skipping...")
            continue
        
        # Use reference stats if available, otherwise use actual data
        if reference_stats and feature in reference_stats:
            ref_data_for_test = np.array(reference_stats[feature]['data'])
        else:
            ref_data_for_test = reference_data.values
        
        drifted, summary = detect_numerical_drift(ref_data_for_test, new_data.values, feature)
        
        drift_results[feature] = summary
        any_drift = any_drift or drifted
        
        # Print results
        status = "🔴 DRIFT DETECTED" if drifted else "✅ OK"
        print(f"\n{status} - Feature: '{feature}'")
        print(f"  KS Statistic: {summary['ks_statistic']:.4f}")
        print(f"  P-Value: {summary['p_value']:.4f}")
        print(f"  Reference: mean={summary['ref_mean']:.2f}, std={summary['ref_std']:.2f}")
        print(f"  New Data:   mean={summary['new_mean']:.2f}, std={summary['new_std']:.2f}")
        print(f"  Mean Shift: {summary['mean_shift']:.2f}σ, Std Shift: {summary['std_shift']:.2f}σ")
    
    # Check categorical feature
    if TEXT_FEATURE in df_reference.columns and TEXT_FEATURE in df_new.columns:
        print(f"\n📋 Checking categorical feature: '{TEXT_FEATURE}'...")
        print("-" * 60)
        
        reference_data = df_reference[TEXT_FEATURE]
        new_data = df_new[TEXT_FEATURE]
        
        # Get reference distribution
        if reference_stats and TEXT_FEATURE in reference_stats:
            ref_counts = reference_stats[TEXT_FEATURE]['value_counts']
        else:
            ref_counts = reference_data.value_counts().to_dict()
        
        drifted, summary = detect_categorical_drift(ref_counts, new_data, TEXT_FEATURE)
        
        drift_results[TEXT_FEATURE] = summary
        any_drift = any_drift or drifted
        
        # Print results
        status = "🔴 DRIFT DETECTED" if drifted else "✅ OK"
        print(f"\n{status} - Feature: '{TEXT_FEATURE}'")
        print(f"  Chi² Statistic: {summary.get('chi2_statistic', 'N/A'):.4f}")
        print(f"  P-Value: {summary.get('p_value', 'N/A'):.4f}")
        print(f"  Reference Distribution: {summary.get('reference_distribution', {})}")
        print(f"  New Distribution: {summary.get('new_distribution', {})}")
    
    return drift_results, any_drift


def main():
    """Main function to run drift detection."""
    print("=" * 60)
    print("Data Drift Detection Script")
    print("=" * 60)
    print()
    
    # Load data
    print("📁 Loading data...")
    try:
        df = pd.read_csv(DATA_FILE_PATH, encoding='latin1')
        print(f"✅ Loaded {len(df)} rows from {DATA_FILE_PATH}")
    except Exception as e:
        print(f"❌ Error loading data: {e}")
        return
    
    # Check if reference statistics exist
    reference_stats = load_reference_statistics()
    
    if reference_stats:
        print(f"✅ Loaded reference statistics from {REFERENCE_STATS_FILE}")
        print("   Using saved training data statistics as reference.")
        # We still need to load training data for comparison
        # But we'll use the saved stats for the actual tests
    else:
        print("ℹ️  No saved reference statistics found.")
        print("   Will calculate from training data split.")
    
    # Split data into train/test (same logic as train.py)
    print("\n📊 Splitting data (80% train, 20% test)...")
    
    # For each city, split the data
    all_train_indices = []
    all_test_indices = []
    
    for city in CLIENT_CITIES:
        city_df = df[df['city'] == city].copy()
        if len(city_df) == 0:
            continue
        
        indices = np.arange(len(city_df))
        train_indices, test_indices = train_test_split(
            indices, test_size=0.2, random_state=42
        )
        
        # Map back to original dataframe indices
        city_start_idx = city_df.index[0]
        all_train_indices.extend(city_df.index[train_indices])
        all_test_indices.extend(city_df.index[test_indices])
    
    df_train = df.loc[all_train_indices].copy()
    df_test = df.loc[all_test_indices].copy()
    
    print(f"✅ Training data: {len(df_train)} rows")
    print(f"✅ Test data: {len(df_test)} rows")
    
    # Calculate and save reference statistics if not already saved
    if not reference_stats:
        print("\n📊 Calculating reference statistics from training data...")
        reference_stats = calculate_reference_statistics(df_train)
        save_reference_statistics(reference_stats)
    
    # Run drift detection
    print("\n" + "=" * 60)
    drift_results, any_drift = run_drift_detection(df_train, df_test, reference_stats)
    
    # Print summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    drifted_features = [f for f, r in drift_results.items() if r.get('drifted', False)]
    stable_features = [f for f, r in drift_results.items() if not r.get('drifted', False)]
    
    print(f"\n✅ Stable features ({len(stable_features)}): {', '.join(stable_features[:5])}")
    if len(stable_features) > 5:
        print(f"   ... and {len(stable_features) - 5} more")
    
    if drifted_features:
        print(f"\n🔴 Features with drift ({len(drifted_features)}): {', '.join(drifted_features)}")
        print("\n⚠️  RECOMMENDATION: Model retraining may be necessary!")
        print("   Consider running: python run_distributed_fl.py")
    else:
        print("\n✅ All features are stable. No drift detected.")
        print("   Model is performing on data similar to training data.")
    
    print("\n" + "=" * 60)
    
    return any_drift


if __name__ == "__main__":
    main()
