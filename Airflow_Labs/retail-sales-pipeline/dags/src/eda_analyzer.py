import pandas as pd
import numpy as np
import pickle
import json
import os

def perform_eda(data):
    """Perform basic EDA."""
    print("Performing EDA...")
    train = data['train']
    
    eda_results = {
        'basic_stats': {
            'sales_mean': float(train['Item_Outlet_Sales'].mean()),
            'sales_median': float(train['Item_Outlet_Sales'].median())
        },
        'missing_values': train.isnull().sum().to_dict()
    }
    
    reports_dir = os.path.join(os.path.dirname(__file__), "../reports")
    os.makedirs(reports_dir, exist_ok=True)
    
    with open(os.path.join(reports_dir, 'eda_report.json'), 'w') as f:
        json.dump(eda_results, f, indent=2)
    
    print("EDA completed")
    return eda_results
