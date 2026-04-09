import argparse
import itertools
import pandas as pd
import numpy as np
from scipy.stats import spearmanr
from collections import defaultdict


def generate_weight_combinations(features, step=0.1):
    """
    Generates all possible combinations of weights for the given features
    where the sum of the weights equals 1.0.
    """
    num_features = len(features)
    n_steps = int(round(1.0 / step))
    
    combinations = []
    # Using stars and bars / combinations with replacement approach 
    # to find non-negative integers summing to n_steps
    for combo in itertools.combinations_with_replacement(range(num_features), n_steps):
        counts = [0] * num_features
        for idx in combo:
            counts[idx] += 1
        
        weights = [c * step for c in counts]
        # ensure floating point math sum exactly to 1.0 isn't an issue
        combinations.append(weights)
        
    return [dict(zip(features, w)) for w in combinations]


def calculate_pipeline_score(row, weights):
    """
    Calculates the final similarity score based on the current weight set.
    Assuming higher is more similar. Adjust calculations based on actual feature scaling.
    """
    score = 0.0
    for feature, weight in weights.items():
        if pd.notna(row.get(feature)):
            score += row[feature] * weight
    return score


def grid_search_best_parameters(df, feature_cols, label_col='label', step=0.1):
    """
    Evaluates all weight combinations using Spearman's Rank Correlation
    against the human label to find the optimal weights.
    """
    print(f"Starting Grid Search with {len(df)} samples...")
    print(f"Features involved: {feature_cols}")
    
    weight_grids = generate_weight_combinations(feature_cols, step=step)
    print(f"Generated {len(weight_grids)} parameter combinations to evaluate.")
    
    results = []
    
    labels = df[label_col].values
    
    for i, w_dict in enumerate(weight_grids):
        # Calculate combined score for this weight
        combined_scores = df.apply(lambda row: calculate_pipeline_score(row, w_dict), axis=1).values
        
        # Method A: Calculate Spearman's Rank Correlation (rho)
        rho, p_value = spearmanr(labels, combined_scores, nan_policy='omit')
        
        results.append({
            'weights': w_dict,
            'spearman_rho': rho,
            'p_value': p_value
        })
        
        if (i+1) % 50 == 0:
            print(f"Evaluated {i+1}/{len(weight_grids)} combinations...")
            
    # Sort by Spearman correlation descending (higher positive correlation is better)
    # We want labels 0,1,2,3 to strictly map to higher similarity scores.
    results.sort(key=lambda x: x['spearman_rho'] if not np.isnan(x['spearman_rho']) else -1, reverse=True)
    
    return results


def main():
    parser = argparse.ArgumentParser(description="Similarity Metric Hyperparameter Search")
    parser.add_argument('--data', type=str, help='Path to the CSV containing raw features and labels')
    parser.add_argument('--step', type=float, default=0.1, help='Grid search step size (e.g. 0.1)')
    args = parser.parse_args()

    # Features that your similarity pipeline uses
    # (Must match the column names in your CSV)
    feature_cols = ['score_hash', 'score_mse', 'score_ssim', 'score_mobilenet']

    if args.data:
        print(f"Loading data from {args.data}...")
        df = pd.read_csv(args.data)
        missing_cols = [c for c in feature_cols + ['label'] if c not in df.columns]
        if missing_cols:
            print(f"ERROR: Missing columns in the dataset: {missing_cols}")
            print(f"Please ensure your dataset exports these raw features so parameter tuning can run offline.")
            return
            
        df = df.dropna(subset=feature_cols + ['label'])
    else:
        # Generate some dummy data to demonstrate the concept to the professor
        print("\n[NOTICE] No data file provided. Generating some synthetic MOCK data to demonstrate the algorithm...\n")
        np.random.seed(42)
        n_samples = 100
        labels = np.random.choice([0, 1, 2, 3], n_samples)
        
        # Create fake features where score_mobilenet is a very good predictor, 
        # score_hash is decent, and score_mse is noisy.
        df = pd.DataFrame({
            'label': labels,
            'score_hash': labels * 20 + np.random.normal(0, 10, n_samples),
            'score_mse': labels * 5 + np.random.normal(0, 20, n_samples),
            'score_ssim': labels * 15 + np.random.normal(0, 15, n_samples),
            'score_mobilenet': labels * 25 + np.random.normal(0, 5, n_samples), 
        })
        # Normalize fake features to 0-100 range roughly
        for col in feature_cols:
            df[col] = (df[col] - df[col].min()) / (df[col].max() - df[col].min()) * 100

    results = grid_search_best_parameters(df, feature_cols, label_col='label', step=args.step)
    
    print("\n" + "="*50)
    print("🏆 TOP 5 PARAMETER COMBINATIONS 🏆")
    print("="*50)
    for i in range(min(5, len(results))):
        w = results[i]
        weight_str = ", ".join([f"{k}: {v:.2f}" for k, v in w['weights'].items()])
        print(f"Rank {i+1}: Spearman's ρ = {w['spearman_rho']:.4f} (p-value={w['p_value']:.2e})")
        print(f"         Weights -> {weight_str}\n")

if __name__ == "__main__":
    main()
