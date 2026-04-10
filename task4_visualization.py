"""
Task 4 — Visualizations
TrendPulse Project

This script:
1. Loads analysed CSV data (Task 3)
2. Creates 3 charts using Matplotlib
3. Saves each chart as PNG
4. Combines them into a dashboard
"""

import pandas as pd
import matplotlib.pyplot as plt
import os

# -----------------------------
# STEP 1: LOAD DATA + SETUP
# -----------------------------

file_path = "data/trends_analysed.csv"

try:
    df = pd.read_csv(file_path)
    print("Data loaded successfully!")
except Exception as e:
    print("Error loading file:", e)
    exit()

# Create outputs folder
os.makedirs("outputs", exist_ok=True)


# -----------------------------
# HELPER FUNCTION
# -----------------------------

# Shorten long titles (for better display)
def shorten_title(title, max_len=50):
    return title[:max_len] + "..." if len(title) > max_len else title


# -----------------------------
# CHART 1: TOP 10 STORIES
# -----------------------------

# Sort and take top 10
top10 = df.sort_values(by="score", ascending=False).head(10)

# Shorten titles
top10["short_title"] = top10["title"].apply(shorten_title)

plt.figure()

plt.barh(top10["short_title"], top10["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")

plt.gca().invert_yaxis()  # highest at top

# Save chart
plt.savefig("outputs/chart1_top_stories.png")
plt.close()


# -----------------------------
# CHART 2: STORIES PER CATEGORY
# -----------------------------

category_counts = df["category"].value_counts()

plt.figure()

plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Stories per Category")

# Save chart
plt.savefig("outputs/chart2_categories.png")
plt.close()


# -----------------------------
# CHART 3: SCATTER PLOT
# -----------------------------

plt.figure()

# Separate popular vs non-popular
popular = df[df["is_popular"] == True]
not_popular = df[df["is_popular"] == False]

plt.scatter(popular["score"], popular["num_comments"], label="Popular")
plt.scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")

plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Comments")

plt.legend()

# Save chart
plt.savefig("outputs/chart3_scatter.png")
plt.close()


# -----------------------------
# BONUS: DASHBOARD
# -----------------------------

fig, axes = plt.subplots(1, 3, figsize=(18, 5))

# Chart 1 (Top stories)
axes[0].barh(top10["short_title"], top10["score"])
axes[0].set_title("Top 10 Stories")
axes[0].set_xlabel("Score")
axes[0].invert_yaxis()

# Chart 2 (Categories)
axes[1].bar(category_counts.index, category_counts.values)
axes[1].set_title("Stories per Category")
axes[1].set_xlabel("Category")

# Chart 3 (Scatter)
axes[2].scatter(popular["score"], popular["num_comments"], label="Popular")
axes[2].scatter(not_popular["score"], not_popular["num_comments"], label="Not Popular")
axes[2].set_title("Score vs Comments")
axes[2].set_xlabel("Score")
axes[2].set_ylabel("Comments")
axes[2].legend()

# Overall title
plt.suptitle("TrendPulse Dashboard")

# Save dashboard
plt.savefig("outputs/dashboard.png")
plt.close()

print("All charts saved in 'outputs/' folder!")
