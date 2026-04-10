"""
Task 3 — Analysis with Pandas & NumPy
TrendPulse Project

This script:
1. Loads cleaned CSV data from Task 2
2. Performs analysis using Pandas and NumPy
3. Adds new calculated columns
4. Saves the updated dataset
"""

import pandas as pd
import numpy as np
import os

# -----------------------------
# STEP 1: LOAD AND EXPLORE DATA
# -----------------------------

file_path = "data/trends_clean.csv"

try:
    df = pd.read_csv(file_path)
    print(f"Loaded data: {df.shape}")
except Exception as e:
    print("Error loading file:", e)
    exit()

# Display first 5 rows
print("\nFirst 5 rows:")
print(df.head())

# Average score and comments
avg_score = df["score"].mean()
avg_comments = df["num_comments"].mean()

print(f"\nAverage score   : {avg_score:.2f}")
print(f"Average comments: {avg_comments:.2f}")

# -----------------------------
# STEP 2: NUMPY ANALYSIS
# -----------------------------

print("\n--- NumPy Stats ---")

scores = df["score"].values

# Mean, Median, Std
mean_score = np.mean(scores)
median_score = np.median(scores)
std_score = np.std(scores)

print(f"Mean score   : {mean_score:.2f}")
print(f"Median score : {median_score:.2f}")
print(f"Std deviation: {std_score:.2f}")

# Max and Min
max_score = np.max(scores)
min_score = np.min(scores)

print(f"Max score    : {max_score}")
print(f"Min score    : {min_score}")

# Category with most stories
category_counts = df["category"].value_counts()
top_category = category_counts.idxmax()
top_count = category_counts.max()

print(f"\nMost stories in: {top_category} ({top_count} stories)")

# Most commented story
max_comments_idx = df["num_comments"].idxmax()
top_story_title = df.loc[max_comments_idx, "title"]
top_story_comments = df.loc[max_comments_idx, "num_comments"]

print(f"\nMost commented story: \"{top_story_title}\" — {top_story_comments} comments")

# -----------------------------
# STEP 3: ADD NEW COLUMNS
# -----------------------------

# Engagement = comments per score
df["engagement"] = df["num_comments"] / (df["score"] + 1)

# Popular flag
df["is_popular"] = df["score"] > avg_score

# -----------------------------
# STEP 4: SAVE RESULT
# -----------------------------

os.makedirs("data", exist_ok=True)
output_file = "data/trends_analysed.csv"

df.to_csv(output_file, index=False)

print(f"\nSaved to {output_file}")
