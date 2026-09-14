import requests
import json
from datetime import datetime, timezone
from pathlib import Path
TOP_STORIES_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"
response = requests.get(TOP_STORIES_URL, timeout=(5,5))
response.raise_for_status()
story_ids = response.json()
story_ids = story_ids[:500]
stories = []
CATEGORY_KEYWORDS = {
    "technology": [
        "ai", "software", "programming", "computer", "chip", "cloud",
        "technology", "tech", "developer", "code", "coding", "data",
        "database", "internet", "web", "app", "startup", "linux",
        "github", "python", "javascript", "server", "security", "cyber",
        "robot", "robotics", "machine learning", "open source",
        "browser", "iphone", "android", "julia", "cuda", "driver",
        "drivers", "duckdb", "sql", "rust", "ide", "terminal",
        "compiler", "algorithm", "css", "react", "postgres",
        "macos", "windows", "openstreetmap", "qemu", "emacs",
        "semiconductor", "llm", "gpt", "transformer", "model",
        "artificial intelligence"
    ],

    "worldnews": [
        "election", "government", "war", "president", "policy",
        "country", "minister", "politics", "political", "congress",
        "parliament", "china", "india", "russia", "ukraine", "israel",
        "iran", "europe", "america", "united states", "uk", "law",
        "court", "military", "protest", "vote", "voting", "democracy",
        "sanctions", "border", "warfare", "conflict", "crisis",
        "presidential", "politician", "politicians", "foreign",
        "international", "geopolitics", "diplomacy", "treaty",
        "refugee", "immigration", "nato", "un", "supreme court"
    ],

    "sports": [
        "cricket", "olympics", "tennis", "football", "basketball",
        "soccer", "baseball", "sports", "sport", "match", "player",
        "team", "league", "championship", "tournament", "world cup",
        "premier league", "nba", "nfl", "fifa", "athlete", "coach",
        "goal", "race", "racing", "golf", "hockey", "formula 1", "f1",
        "medal", "champion", "runner", "running", "marathon", "cycling",
        "cyclist", "boxing", "wrestling", "volleyball", "rugby",
        "swimming", "skiing", "skier", "snowboard", "badminton",
        "champions", "athletics", "cup", "final", "semifinal",
        "playoff", "playoffs", "season", "score", "scoring"
    ],

    "science": [
        "research", "nasa", "space", "physics", "biology", "climate",
        "science", "scientist", "study", "scientists", "astronomy",
        "chemistry", "laboratory", "experiment", "discovery", "planet",
        "earth", "moon", "mars", "energy", "environment", "evolution",
        "genetics", "quantum", "telescope", "medical", "medicine",
        "health", "vaccine", "cell", "dna", "mathematics",
        "mathematical", "math", "theorem", "radiation", "orbit",
        "orbits", "astronomical", "physicist", "biological",
        "dinosaur", "dinosaurs", "glacier", "glaciers",
        "hurricane", "hurricanes", "battery", "nuclear",
        "intelligence"
    ],

    "entertainment": [
        "movie", "music", "actor", "film", "tv", "game", "entertainment",
        "actress", "cinema", "series", "television", "netflix",
        "youtube", "spotify", "album", "song", "singer", "director",
        "hollywood", "show", "gaming", "videogame", "comedy",
        "celebrity", "concert", "band", "podcast", "anime", "book",
        "author"
    ]
}
def match_category(title):
    title = str(title).lower()

    for category, keywords in CATEGORY_KEYWORDS.items():
        if any(keyword in title for keyword in keywords):
            return category

    return None
category_counts = {
    "technology": 0,
    "worldnews": 0,
    "sports": 0,
    "science": 0,
    "entertainment": 0
}

for story_id in story_ids:

    try:
        response = requests.get(
            ITEM_URL.format(story_id),
            timeout=10
        )
        response.raise_for_status()
        story = response.json()

    except requests.RequestException:
        continue

    title = story.get("title")
    category = match_category(title)
    if category is None:
     continue
    if category_counts[category] >= 25:
        continue

    post_id = story.get("id")
    score = story.get("score")
    num_comments = story.get("descendants", 0)
    author = story.get("by")
    collected_at = datetime.now(timezone.utc).isoformat()

    story_data = {
        "post_id": post_id,
        "title": title,
        "category": category,
        "score": score,
        "num_comments": num_comments,
        "author": author,
        "collected_at": collected_at
    }

    stories.append(story_data)

    category_counts[category] += 1

    if len(stories) >= 100:
        break
if len(stories) < 100:
    raise RuntimeError(
        f"Only {len(stories)} stories were collected. "
        "At least 100 stories are required."
    )
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)
date_string = datetime.now(timezone.utc).strftime("%Y%m%d")
output_file = data_folder / f"trends_{date_string}.json"
with open(output_file, "w", encoding="utf-8") as file:
    json.dump(
        stories,
        file,
        indent=4,
        ensure_ascii=False
    )
print(f"Collected stories: {len(stories)}")
print("Category counts:")
for category, count in category_counts.items():
    print(f"{category}: {count}")
print(f"Saved file: {output_file}")

