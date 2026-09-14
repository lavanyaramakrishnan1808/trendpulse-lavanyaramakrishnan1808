import pandas as pd
from pathlib import Path
import glob
json_files = glob.glob("data/trends_*.json")
if not json_files:
    raise FileNotFoundError("No raw JSON file found in the data folder.")
input_file = json_files[0]
clean = pd.read_json(input_file)
clean = clean.drop_duplicates(subset="post_id")
clean = clean.dropna(subset=["post_id", "title", "score"])
clean["score"] = pd.to_numeric(clean["score"], errors="coerce")
clean["num_comments"] = pd.to_numeric(
    clean["num_comments"],
    errors="coerce")
clean = clean.dropna(subset=["score"])
clean = clean[clean["score"] >= 5]
clean["title"] = clean["title"].str.strip()
clean["score"] = clean["score"].astype(int)
clean["num_comments"] = clean["num_comments"].fillna(0).astype(int)
data_folder = Path("data")
data_folder.mkdir(exist_ok=True)
output_file = data_folder / "trends_clean.csv"
clean.to_csv(output_file, index=False)
print(f"Cleaned stories: {len(clean)}")
print("\nStories by category:")
print(clean["category"].value_counts())
print(f"\nSaved file: {output_file}")