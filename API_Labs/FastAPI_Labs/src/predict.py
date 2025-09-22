import joblib

model = joblib.load("../model/spam_model.pkl")
vectorizer = joblib.load("../model/tfidf_vectorizer.pkl")

def predict_data(text):
    """
    Predict the class labels for the input data.
    Args:
        X (numpy.ndarray): Input data for which predictions are to be made.
    Returns:
        y_pred (numpy.ndarray): Predicted class labels.
    """
    X = vectorizer.transform([text])
    pred = model.predict(X)[0]
    return "spam" if pred == 1 else "ham"
