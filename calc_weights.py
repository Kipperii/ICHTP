import csv
import math

def main():
    file_path = r'c:\Users\Administrator\Desktop\ICHTP\scripts\labeled_pairs_merged.csv'
    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        rows = [r for r in reader if r['score_hash'] and r['label']]
        
    labels = [float(r['label']) for r in rows]
    hash_scores = [float(r['score_hash']) for r in rows]
    mse_scores = [float(r['score_mse']) for r in rows]
    ssim_scores = [float(r['score_ssim']) for r in rows]
    ai_scores = [float(r['score_mobilenet']) for r in rows]
    current_sim_scores = [float(r['similarity_score']) for r in rows]
    
    # Calculate simple Pearson Correlation
    def pearson(x, y):
        n = len(x)
        mx = sum(x)/n
        my = sum(y)/n
        cov = sum((x[i]-mx)*(y[i]-my) for i in range(n))
        varx = sum((x[i]-mx)**2 for i in range(n))
        vary = sum((y[i]-my)**2 for i in range(n))
        if varx == 0 or vary == 0: return 0
        return cov / math.sqrt(varx * vary)

    print("=== Correlation with Human Label (0 to 3) ===")
    print(f"Hash Dist (lower is similar): {pearson(labels, hash_scores):.4f}")
    print(f"MSE (lower is similar):     {pearson(labels, mse_scores):.4f}")
    print(f"SSIM (higher is similar):    {pearson(labels, ssim_scores):.4f}")
    print(f"MobileNet (higher is sim):   {pearson(labels, ai_scores):.4f}")
    print(f"Current Pipeline Score:      {pearson(labels, current_sim_scores):.4f}")

    # Optimize weights using basic least squares (Multiple Linear Regression)
    # y = w0 + w1*(1 - hash_normalized) + w2*(1 - mse_normalized) + w3*ssim + w4*ai
    # Normalize features to 0-1 for easier interpretation
    
    def normalize(x, inverted=False):
        min_x = min(x)
        max_x = max(x)
        if max_x == min_x: return [0]*len(x)
        res = [(v - min_x) / (max_x - min_x) for v in x]
        if inverted:
            res = [1.0 - v for v in res]
        return res
        
    n_hash = normalize(hash_scores, inverted=True) # smaller hash = higher sim
    n_mse = normalize(mse_scores, inverted=True)   # smaller mse = higher sim
    n_ssim = normalize(ssim_scores, inverted=False) 
    n_ai = normalize(ai_scores, inverted=False)
    
    # Simple Gradient Descent to find best weights that sum to 1 (ignoring intercept for a strict combined score)
    # Objective: Minimize squared error between predicted score (scaled to 0-3) and label
    w_hash, w_mse, w_ssim, w_ai = 0.25, 0.25, 0.25, 0.25
    lr = 0.01
    for epoch in range(10000):
        grad_hash = grad_mse = grad_ssim = grad_ai = 0
        total_loss = 0
        for i in range(len(labels)):
            y_pred = 3.0 * (w_hash * n_hash[i] + w_mse * n_mse[i] + w_ssim * n_ssim[i] + w_ai * n_ai[i])
            err = y_pred - labels[i]
            total_loss += err**2
            grad_hash += err * 3.0 * n_hash[i]
            grad_mse += err * 3.0 * n_mse[i]
            grad_ssim += err * 3.0 * n_ssim[i]
            grad_ai += err * 3.0 * n_ai[i]
        
        w_hash -= lr * grad_hash / len(labels)
        w_mse -= lr * grad_mse / len(labels)
        w_ssim -= lr * grad_ssim / len(labels)
        w_ai -= lr * grad_ai / len(labels)
        
        # Softmax / normalize to keep sum=1 and >0
        w_hash = max(0, w_hash)
        w_mse = max(0, w_mse)
        w_ssim = max(0, w_ssim)
        w_ai = max(0, w_ai)
        s = w_hash + w_mse + w_ssim + w_ai
        if s > 0:
            w_hash /= s
            w_mse /= s
            w_ssim /= s
            w_ai /= s
            
    print("\n=== Optimized Weights (Sum to 1) ===")
    print(f"Hash config equivalent (diversityW): {w_hash:.4f}")
    print(f"MSE config equivalent (mseW):        {w_mse:.4f}")
    print(f"SSIM config equivalent (ssimW):      {w_ssim:.4f}")
    print(f"AI config equivalent (aiW):          {w_ai:.4f}")
    
    # Calculate performance of new weights
    new_scores = [w_hash*n_hash[i] + w_mse*n_mse[i] + w_ssim*n_ssim[i] + w_ai*n_ai[i] for i in range(len(labels))]
    print(f"Optimized Pipeline Correlation:      {pearson(labels, new_scores):.4f}")

if __name__ == '__main__':
    main()