import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.feature_extraction.text import TfidfVectorizer
import joblib
import os

def load_data():
    # Download SMS Spam Collection dataset from GitHub raw url
    url = "https://raw.githubusercontent.com/justmarkham/pycon-2016-tutorial/master/data/sms.tsv"
    df = pd.read_csv(url, sep="\t", header=None, names=["label", "message"])

    # Map 'ham' -> 0, 'spam' -> 1
    df['label'] = df['label'].map({'ham': 0, 'spam': 1})

    return df['message'], df['label']

def split_data(X, y, test_size=0.2, random_state=42):
    X_train_raw, X_test_raw, y_train, y_test = train_test_split(X, y, test_size=test_size, random_state=random_state)
    
    # Fit TF-IDF on training data, transform both train and test
    vectorizer = TfidfVectorizer(stop_words='english')
    X_train = vectorizer.fit_transform(X_train_raw)
    X_test = vectorizer.transform(X_test_raw)

    # Save vectorizer for later use (important!)
    os.makedirs("../model", exist_ok=True)
    joblib.dump(vectorizer, "../model/tfidf_vectorizer.pkl")

    return X_train, X_test, y_train, y_test
