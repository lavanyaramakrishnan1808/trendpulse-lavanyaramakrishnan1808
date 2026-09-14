import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("data/trends_analysed.csv")
top_stories = data.sort_values("score", ascending=False).head(10)
plt.figure(figsize=(10, 6))
plt.barh(top_stories["title"], top_stories["score"])
plt.xlabel("Score")
plt.ylabel("Story Title")
plt.title("Top 10 Stories by Score")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("outputs/chart1_top_stories.png")
plt.show()
category_counts = data["category"].value_counts()
plt.figure(figsize=(8, 5))
plt.bar(category_counts.index, category_counts.values)
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.title("Number of Stories by Category")
plt.tight_layout()
plt.savefig("outputs/chart2_categories.png")
plt.show()
popular_stories = data[data["is_popular"] == True]
normal_stories = data[data["is_popular"] == False]
plt.figure(figsize=(8, 5))
plt.scatter(
    normal_stories["score"],
    normal_stories["num_comments"],
    label="Not Popular"
)
plt.scatter(
    popular_stories["score"],
    popular_stories["num_comments"],
    label="Popular"
)
plt.xlabel("Score")
plt.ylabel("Number of Comments")
plt.title("Score vs Number of Comments")
plt.legend()
plt.tight_layout()
plt.savefig("outputs/chart3_scatter.png")
plt.show()
print("All charts have been created successfully.")