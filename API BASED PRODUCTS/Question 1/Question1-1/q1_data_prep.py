import pandas as pd
from utils import calculate_cosine_similarity

# Simulated training data with various similarity levels
data = [
    # High similarity (plagiarized)
    ("This is the original sentence.", "This is the original sentence.", 1),
    ("The sky is blue and beautiful.", "The sky is blue and beautiful today.", 1),
    ("Machine learning is an exciting field of study.", "Machine learning is an exciting area of research.", 1),
    ("Python is a great programming language.", "Python is an excellent programming language.", 1),
    ("Data science combines statistics and programming.", "Data science merges statistics with programming.", 1),
    ("Artificial intelligence is transforming industries.", "AI is transforming various industries.", 1),
    ("Deep learning requires large datasets.", "Deep learning needs large amounts of data.", 1),
    ("The quick brown fox jumps over the lazy dog.", "The quick brown fox jumps over the lazy dog.", 1),
    
    # Low similarity (not plagiarized)
    ("Machine learning is fun.", "I like pizza and pasta.", 0),
    ("Python is a great language.", "I use Java for backend development.", 0),
    ("The weather is nice today.", "Apples are very tasty fruits.", 0),
    ("I enjoy reading books.", "Swimming is a good exercise.", 0),
    ("Coffee tastes bitter.", "The mountain is very tall.", 0),
    ("Cars need fuel to run.", "Music is soothing to ears.", 0),
    ("Trees provide oxygen.", "Computers process information quickly.", 0),
    ("The ocean is deep.", "Birds can fly in the sky.", 0),
]

# Compute similarity scores and create dataset
rows = []
for original, submission, label in data:
    sim = calculate_cosine_similarity(original, submission)
    rows.append([original, submission, sim, label])

# Create DataFrame
df = pd.DataFrame(rows, columns=["Original", "Submission", "Similarity", "Label"])

# Save to CSV
df.to_csv("plagiarism_dataset.csv", index=False)

print("Dataset created successfully!")
print(f"Total samples: {len(df)}")
print(f"Plagiarized samples: {df['Label'].sum()}")
print(f"Original samples: {len(df) - df['Label'].sum()}")
print("\nDataset preview:")
print(df.head(10))