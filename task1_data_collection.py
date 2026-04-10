import requests
import time
import os
import json
from datetime import datetime

# Base URLs
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header (as required)
headers = {"User-Agent": "TrendPulse/1.0"}

# Category keywords (case-insensitive)
CATEGORIES = {
    "technology": ["ai", "software", "tech", "code", "computer", "data", "cloud", "api", "gpu", "llm"],
    "worldnews": ["war", "government", "country", "president", "election", "climate", "attack", "global"],
    "sports": ["nfl", "nba", "fifa", "sport", "game", "team", "player", "league", "championship"],
    "science": ["research", "study", "space", "physics", "biology", "discovery", "nasa", "genome"],
    "entertainment": ["movie", "film", "music", "netflix", "game", "book", "show", "award", "streaming"]
}

# Function to assign category based on title
def get_category(title):
    title_lower = title.lower()
    for category, keywords in CATEGORIES.items():
        for keyword in keywords:
            if keyword in title_lower:
                return category
    return None  # ignore if no category matched


def fetch_data():
    try:
        # Step 1: Fetch top story IDs
        response = requests.get(TOP_STORIES_URL, headers=headers)
        story_ids = response.json()[:500]  # first 500 IDs
    except Exception as e:
        print("Failed to fetch top stories:", e)
        return

    collected_data = []
    category_counts = {cat: 0 for cat in CATEGORIES}

    # Loop through each category separately
    for category in CATEGORIES:
        print(f"\nCollecting {category} stories...")

        for story_id in story_ids:
            # Stop when we reach 25 per category
            if category_counts[category] >= 25:
                break

            try:
                res = requests.get(ITEM_URL.format(story_id), headers=headers)
                story = res.json()

                # Skip invalid stories
                if not story or "title" not in story:
                    continue

                title = story.get("title", "")

                # Check if story belongs to this category
                assigned_category = get_category(title)

                if assigned_category == category:
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

            except Exception as e:
                print(f"Error fetching story {story_id}: {e}")
                continue

        # Wait 2 seconds AFTER each category loop (important requirement)
        time.sleep(2)

    # Step 3: Save to JSON file
    os.makedirs("data", exist_ok=True)

    filename = f"data/trends_{datetime.now().strftime('%Y%m%d')}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")


# Run script
if __name__ == "__main__":
    fetch_data()
