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
    ("Weather is nice today.", "Apples are tasty.", 0),
    ("Artificial intelligence will change the world.", "AI technology is transforming industries.", 1),
    ("I enjoy reading books.", "Cooking is my hobby.", 0),
    ("The sun rises in the east.", "The sun rises in the east every morning.", 1),
]

# Compute similarity and label
rows = []
for original, submission, label in data:
    sim = calculate_cosine_similarity(original, submission)
    rows.append([original, submission, sim, label])

df = pd.DataFrame(rows, columns=["Original", "Submission", "Similarity", "Label"])
df.to_csv("plagiarism_dataset.csv", index=False)
print("Dataset created successfully!")
print(f"Total samples: {len(df)}")
print(df.head())

