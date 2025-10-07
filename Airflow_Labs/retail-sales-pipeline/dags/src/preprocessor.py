import pandas as pd
import numpy as np
from sklearn.preprocessing import LabelEncoder
import pickle

def preprocess_data(data):
    """Preprocess the data."""
    print("Preprocessing data...")
    train = data['train'].copy()
    test = data['test'].copy()
    
    # Basic preprocessing
    for df in [train, test]:
        df['Item_Weight'].fillna(df['Item_Weight'].mean(), inplace=True)
        df['Outlet_Size'].fillna('Medium', inplace=True)
        df['Outlet_Years'] = 2013 - df['Outlet_Establishment_Year']
    
    # Simple encoding
    categorical_cols = ['Item_Fat_Content', 'Outlet_Size', 'Outlet_Location_Type', 'Outlet_Type']
    
    train = pd.get_dummies(train, columns=categorical_cols)
    test = pd.get_dummies(test, columns=categorical_cols)
    
    # Align columns
    test = test.reindex(columns=train.columns, fill_value=0)
    if 'Item_Outlet_Sales' in test.columns:
        test.drop('Item_Outlet_Sales', axis=1, inplace=True)
    
    feature_cols = [col for col in train.columns 
                   if col not in ['Item_Identifier', 'Outlet_Identifier', 'Item_Outlet_Sales', 'Item_Type']]
    
    processed_data = {
        'train': train,
        'test': test,
        'feature_columns': feature_cols,
        'target_column': 'Item_Outlet_Sales',
        'id_columns': ['Item_Identifier', 'Outlet_Identifier']
    }
    
    print(f"Preprocessing complete. Features: {len(feature_cols)}")
    return processed_data
