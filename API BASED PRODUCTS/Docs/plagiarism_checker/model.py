import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
import joblib
from utils import calculate_cosine_similarity

# Load or create data
try:
    df = pd.read_csv("plagiarism_dataset.csv")
except FileNotFoundError:
    print("Dataset not found. Creating dataset...")
    # Create dataset if it doesn't exist
    data = [
        ("The quick brown fox jumps over the lazy dog.", "The quick brown fox jumps over the lazy dog.", 1),
        ("Data science is interesting.", "I love studying data science.", 1),
        ("Python is cool.", "Java is another language.", 0),
        ("Weather is nice today.", "Apples are tasty.", 0),
        ("This is the original sentence.", "This is the original sentence.", 1),
        ("The sky is blue and beautiful.", "The sky is blue.", 1),
        ("Machine learning is fun.", "I like pizza.", 0),
        ("Python is a great language.", "I use Java for backend.", 0),
    ]
    
    rows = []
    for original, submission, label in data:
        sim = calculate_cosine_similarity(original, submission)
        rows.append([sim, label])
    
    df = pd.DataFrame(rows, columns=["similarity", "label"])

X = df[['Similarity']] if 'Similarity' in df.columns else df[['similarity']]
y = df['Label'] if 'Label' in df.columns else df['label']

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

