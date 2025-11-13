"""
ML model training script for plagiarism detection.
"""
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib


# Load data
df = pd.read_csv("plagiarism_dataset.csv")

X = df[['Similarity']]
y = df['Label']

# Split and train
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate
train_score = model.score(X_train, y_train)
test_score = model.score(X_test, y_test)

print(f"Training accuracy: {train_score:.4f}")
print(f"Test accuracy: {test_score:.4f}")

# Save model
joblib.dump(model, 'plagiarism_model.pkl')
print("Model trained and saved as 'plagiarism_model.pkl'")

