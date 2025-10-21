import pickle
import os
import json
import sys
import argparse
import joblib
import numpy as np
from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

sys.path.insert(0, os.path.abspath('..'))
from data_loader import load_data
from preprocessor import preprocess_data


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", type=str, required=True, help="Timestamp from GitHub Actions")
    args = parser.parse_args()
    
    timestamp = args.timestamp
    
    try:
        # Load the trained model
        model_version = f'model_{timestamp}_rf_model'
        model_path = f'../working_data/{model_version}.joblib'
        
        if not os.path.exists(model_path):
            # Try alternative path
            model_path = f'{model_version}.joblib'
        
        model = joblib.load(model_path)
        print(f"Model loaded from: {model_path}")
    except Exception as e:
        raise ValueError(f'Failed to load the model: {e}')
    
    try:
        # Load and preprocess test data
        print("Loading test data...")
        data = load_data()
        processed_data = preprocess_data(data)
        
        # Get test features
        test = processed_data['test']
        feature_columns = processed_data['feature_columns']
        
        # For evaluation, we'll use validation split from training data
        # since test data doesn't have labels
        train = processed_data['train']
        from sklearn.model_selection import train_test_split
        
        X = train[feature_columns]
        y = train[processed_data['target_column']]
        
        _, X_val, _, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
        
        print(f"Evaluating on {len(X_val)} validation samples...")
        
    except Exception as e:
        raise ValueError(f'Failed to load or process the data: {e}')
    
    # Make predictions
    y_predict = model.predict(X_val)
    
    # Calculate metrics
    rmse = np.sqrt(mean_squared_error(y_val, y_predict))
    mae = mean_absolute_error(y_val, y_predict)
    r2 = r2_score(y_val, y_predict)
    
    metrics = {
        "RMSE": float(rmse),
        "MAE": float(mae),
        "R2_Score": float(r2)
    }
    
    print(f"Evaluation Metrics:")
    print(f"  RMSE: {rmse:.2f}")
    print(f"  MAE: {mae:.2f}")
    print(f"  R2 Score: {r2:.4f}")
    
    # Save metrics to a JSON file
    if not os.path.exists('metrics/'): 
        os.makedirs("metrics/")
        
    metrics_filename = f'{timestamp}_metrics.json'
    with open(metrics_filename, 'w') as metrics_file:
        json.dump(metrics, metrics_file, indent=4)
    
    print(f"Metrics saved to: {metrics_filename}")