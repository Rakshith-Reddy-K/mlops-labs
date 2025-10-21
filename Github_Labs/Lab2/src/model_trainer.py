import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error
import pickle
import os

def train_models(data,filename):
    """Train models."""
    print("Training models...")
    train = data['train']
    feature_columns = data['feature_columns']
    target_column = data['target_column']
    
    X = train[feature_columns]
    y = train[target_column]
    
    X_train, X_val, y_train, y_val = train_test_split(X, y, test_size=0.2, random_state=42)
    
    # Train Random Forest
    model = RandomForestRegressor(n_estimators=50, max_depth=10, random_state=42)
    model.fit(X_train, y_train)
    
    val_pred = model.predict(X_val)
    val_rmse = np.sqrt(mean_squared_error(y_val, val_pred))
    
    print(f"Model trained. Validation RMSE: {val_rmse:.2f}")
    
    models_dir = os.path.join(os.path.dirname(__file__), "../../working_data")
    os.makedirs(models_dir, exist_ok=True)
    
    output_path = os.path.join(models_dir, filename)
    print("Output path:", output_path)

    with open(output_path, 'wb') as f:
        pickle.dump(model, f)
    
    return {'results': {'rf': {'val_rmse': val_rmse}}}
