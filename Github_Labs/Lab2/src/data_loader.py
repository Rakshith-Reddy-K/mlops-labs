import pandas as pd
import numpy as np
import pickle
import os
from datetime import datetime

def load_data():
    """Load train and test datasets."""
    print("Loading data...")
    data_path = os.path.join(os.path.dirname(__file__), "../data")
    
    # Check if data exists
    train_path = os.path.join(data_path, "Train.csv")
    test_path = os.path.join(data_path, "Test.csv")
    
    if not os.path.exists(train_path):
        raise FileNotFoundError(f"Training data not found. Please place Train.csv in {data_path}")
    if not os.path.exists(test_path):
        raise FileNotFoundError(f"Test data not found. Please place Test.csv in {data_path}")
    
    train = pd.read_csv(train_path)
    test = pd.read_csv(test_path)
    
    if 'Item_Outlet_Sales' not in test.columns:
        test['Item_Outlet_Sales'] = np.nan
    
    print(f"Loaded {len(train)} training and {len(test)} test samples")
    
    data = {
        'train': train,
        'test': test,
        'metadata': {'train_samples': len(train), 'test_samples': len(test)}
    }
    
    return data
