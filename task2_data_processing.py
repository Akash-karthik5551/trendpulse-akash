"""
Task 2 — Clean the Data & Save as CSV
TrendPulse Project

This script:
1. Loads raw JSON data from Task 1
2. Cleans the data (duplicates, nulls, types, etc.)
3. Saves cleaned data as CSV
4. Prints summary statistics
"""

import pandas as pd
import os

# -----------------------------
# STEP 1: LOAD JSON FILE
# -----------------------------

# File path (update date if needed)
file_path = "data/trends_20260410.json"

# Load JSON into DataFrame
try:
    df = pd.read_json(file_path)
    print(f"Loaded {len(df)} stories from {file_path}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# -----------------------------
# STEP 2: CLEAN THE DATA
# -----------------------------

# 1. Remove duplicate post_id
before = len(df)
df = df.drop_duplicates(subset="post_id")
print(f"After removing duplicates: {len(df)}")

# 2. Remove missing values (important columns)
before = len(df)
df = df.dropna(subset=["post_id", "title", "score"])
print(f"After removing nulls: {len(df)}")

# 3. Fix data types
df["score"] = df["score"].astype(int)
df["num_comments"] = df["num_comments"].astype(int)

# 4. Remove low-quality stories (score < 5)
before = len(df)
df = df[df["score"] >= 5]
print(f"After removing low scores: {len(df)}")

# 5. Clean whitespace in title
df["title"] = df["title"].str.strip()

# -----------------------------
# STEP 3: SAVE CLEANED CSV
# -----------------------------

# Ensure data folder exists
os.makedirs("data", exist_ok=True)

output_file = "data/trends_clean.csv"

# Save to CSV
df.to_csv(output_file, index=False)

print(f"\nSaved {len(df)} rows to {output_file}")

# -----------------------------
# STEP 4: SUMMARY
# -----------------------------

print("\nStories per category:")
print(df["category"].value_counts())
