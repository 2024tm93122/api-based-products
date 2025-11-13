"""
Data preparation script to create training dataset for plagiarism detection model.
"""
import pandas as pd
from utils import calculate_cosine_similarity


# Simulated training data
data = [
    ("This is the original sentence.", "This is the original sentence.", 1),
    ("The sky is blue and beautiful.", "The sky is blue.", 1),
    ("Machine learning is fun.", "I like pizza.", 0),
    ("Python is a great language.", "I use Java for backend.", 0),
    ("The quick brown fox jumps over the lazy dog.", "The quick brown fox jumps over the lazy dog.", 1),
    ("Data science is interesting.", "I love studying data science.", 1),
    ("Python is cool.", "Java is another language.", 0),
    ("Weather is nice today.", "Apples are tasty.", 0),
    ("Artificial intelligence will change the world.", "AI will transform our future.", 1),
    ("I enjoy reading books.", "Cooking is my hobby.", 0),
    ("The sun rises in the east.", "The sun rises in the east every morning.", 1),
    ("Mathematics is difficult.", "I prefer history over science.", 0),
    ("Technology advances rapidly.", "Tech progresses quickly.", 1),
    ("Coffee helps me stay awake.", "I drink tea in the morning.", 0),
    ("Machine learning models require training data.", "ML models need training datasets.", 1),
]


# Compute similarity and label
rows = []
for original, submission, label in data:
    sim = calculate_cosine_similarity(original, submission)
    rows.append([original, submission, sim, label])


df = pd.DataFrame(rows, columns=["Original", "Submission", "Similarity", "Label"])
df.to_csv("plagiarism_dataset.csv", index=False)

print(f"Dataset created with {len(df)} samples.")
print(f"Plagiarized samples: {df['Label'].sum()}")
print(f"Non-plagiarized samples: {len(df) - df['Label'].sum()}")
print("\nFirst few rows:")
print(df.head())

