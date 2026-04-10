import requests
import time
import os
import json
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm", "startup", "programming"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

MAX_PER_CATEGORY = 20  # 20 × 5 = 100


# Assign category
def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None


def fetch_data():
    try:
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json()
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    collected_data = []
    category_counts = {cat: 0 for cat in CATEGORIES}
    used_ids = set()

    print("Collecting categorized stories...\n")

    # -----------------------------
    # STEP 1: Keyword-based collect
    # -----------------------------
    for story_id in story_ids:

        if all(count >= MAX_PER_CATEGORY for count in category_counts.values()):
            break

        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            story = res.json()

            if not story or "title" not in story:
                continue

            title = story.get("title", "")
            category = get_category(title)

            if category and category_counts[category] < MAX_PER_CATEGORY:
                data = {
                    "post_id": story.get("id"),
                    "title": title,
                    "category": category,
                    "score": story.get("score", 0),
                    "num_comments": story.get("descendants", 0),
                    "author": story.get("by", "unknown"),
                    "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }

                collected_data.append(data)
                category_counts[category] += 1
                used_ids.add(story_id)

                print(f"[{category}] {title}")

        except:
            continue

        time.sleep(0.05)

    # -----------------------------
    # STEP 2: Fill remaining slots
    # -----------------------------
    print("\nFilling remaining slots...\n")

    for story_id in story_ids:

        if len(collected_data) >= 100:
            break

        if story_id in used_ids:
            continue

        try:
            res = requests.get(ITEM_URL.format(story_id), headers=headers)
            story = res.json()

            if not story or "title" not in story:
                continue

            # Assign to category with lowest count
            category = min(category_counts, key=category_counts.get)

            data = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by", "unknown"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_data.append(data)
            category_counts[category] += 1

            print(f"[FILL-{category}] {story.get('title')}")

        except:
            continue

        time.sleep(0.05)

    # -----------------------------
    # SAVE FILE
    # -----------------------------
    os.makedirs("data", exist_ok=True)
    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print("\n==============================")
    print("Category Counts:", category_counts)
    print(f"Total Collected: {len(collected_data)}")
    print(f"Saved to: {filename}")


# Run
if __name__ == "__main__":
    fetch_data()
