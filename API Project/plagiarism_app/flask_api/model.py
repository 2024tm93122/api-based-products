"""
ML model training script for plagiarism detection (Flask API version).
"""
import joblib
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from utils import calculate_cosine_similarity


# Example dataset
data = [
    ("The quick brown fox jumps over the lazy dog.", "The quick brown fox jumps over the lazy dog.", 1),
    ("Data science is interesting.", "I love studying data science.", 1),
    ("Python is cool.", "Java is another language.", 0),
    ("Weather is nice today.", "Apples are tasty.", 0),
    ("This is the original sentence.", "This is the original sentence.", 1),
    ("The sky is blue and beautiful.", "The sky is blue.", 1),
    ("Machine learning is fun.", "I like pizza.", 0),
    ("Python is a great language.", "I use Java for backend.", 0),
    ("Artificial intelligence will change the world.", "AI will transform our future.", 1),
    ("I enjoy reading books.", "Cooking is my hobby.", 0),
    ("The sun rises in the east.", "The sun rises in the east every morning.", 1),
    ("Mathematics is difficult.", "I prefer history over science.", 0),
    ("Technology advances rapidly.", "Tech progresses quickly.", 1),
    ("Coffee helps me stay awake.", "I drink tea in the morning.", 0),
    ("Machine learning models require training data.", "ML models need training datasets.", 1),
]


rows = []
for original, submission, label in data:
    sim = calculate_cosine_similarity(original, submission)
    rows.append([sim, label])


df = pd.DataFrame(rows, columns=["similarity", "label"])
X = df[["similarity"]]
y = df["label"]


model = LogisticRegression()
model.fit(X, y)

# Evaluate
score = model.score(X, y)
print(f"Model accuracy: {score:.4f}")

joblib.dump(model, "plagiarism_model.pkl")
print("Model trained and saved as 'plagiarism_model.pkl'")

