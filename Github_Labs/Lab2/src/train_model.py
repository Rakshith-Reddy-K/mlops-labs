import mlflow
import datetime
import os
import pickle
import sys
import argparse
from joblib import dump
from sklearn.metrics import mean_squared_error
import numpy as np

# Import your pipeline modules
sys.path.insert(0, os.path.abspath('..'))
from data_loader import load_data
from preprocessor import preprocess_data
from model_trainer import train_models


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("--timestamp", type=str, required=True, help="Timestamp from GitHub Actions")
    args = parser.parse_args()
    
    timestamp = args.timestamp
    print(f"Timestamp received from GitHub Actions: {timestamp}")
    
    # Set up MLflow
    mlflow.set_tracking_uri("./mlruns")
    dataset_name = "Retail_Sales_Prediction"
    current_time = datetime.datetime.now().strftime("%y%m%d_%H%M%S")
    experiment_name = f"{dataset_name}_{current_time}"    
    experiment_id = mlflow.create_experiment(f"{experiment_name}")

    with mlflow.start_run(experiment_id=experiment_id, run_name=f"{dataset_name}"):
        
        # Load data
        print("Loading data...")
        data = load_data()
        
        # Log data parameters
        params = {
            "dataset_name": dataset_name,
            "train_samples": data['metadata']['train_samples'],
            "test_samples": data['metadata']['test_samples']
        }
        mlflow.log_params(params)
        
        # Preprocess data
        print("Preprocessing data...")
        processed_data = preprocess_data(data)
        
        # Log preprocessing info
        mlflow.log_param("num_features", len(processed_data['feature_columns']))
        
        # Train model
        print("Training model...")
        model_filename = f'model_{timestamp}_rf_model.joblib'
        results = train_models(processed_data, model_filename)
        
        # Log metrics
        val_rmse = results['results']['rf']['val_rmse']
        mlflow.log_metrics({
            'Validation_RMSE': val_rmse
        })
        
        print(f"Model training complete. Validation RMSE: {val_rmse:.2f}")
        print(f"Model saved as: {model_filename}")