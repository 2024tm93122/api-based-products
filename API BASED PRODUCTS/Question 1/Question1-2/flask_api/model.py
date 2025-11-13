import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
import joblib

# Load data
df = pd.read_csv("plagiarism_dataset.csv")

# Features and labels
X = df[['Similarity']]
y = df['Label']

# Split data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42
)

# Train Logistic Regression model
model = LogisticRegression()
model.fit(X_train, y_train)

# Evaluate model
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)

print("=" * 50)
print("Model Training Complete!")
print("=" * 50)
print(f"\nAccuracy: {accuracy * 100:.2f}%")
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=['Original', 'Plagiarized']))
print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# Save model
joblib.dump(model, 'plagiarism_model.pkl')
print("\n✓ Model saved as 'plagiarism_model.pkl'")

# Display model parameters
print(f"\nModel Coefficient: {model.coef_[0][0]:.4f}")
print(f"Model Intercept: {model.intercept_[0]:.4f}")