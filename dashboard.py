import pandas as pd
import matplotlib.pyplot as plt
data = pd.read_csv("data/trends_analysed.csv")
total_stories = len(data)
average_score = data["score"].mean()
average_comments = data["num_comments"].mean()
category_counts = data["category"].value_counts()
top_stories = data.sort_values("score", ascending=False).head(10)
plt.figure(figsize=(16, 10))
plt.subplot(2, 2, 1)
plt.text(
    0.5,
    0.5,
    "Total Stories\n\n" + str(total_stories),
    ha="center",
    va="center",
    fontsize=24
)
plt.axis("off")
plt.subplot(2, 2, 2)
plt.text(
    0.5,
    0.65,
    "Average Score\n" + str(round(average_score, 2)),
    ha="center",
    va="center",
    fontsize=20
)
plt.text(
    0.5,
    0.35,
    "Average Comments\n" + str(round(average_comments, 2)),
    ha="center",
    va="center",
    fontsize=20
)
plt.axis("off")
plt.subplot(2, 2, 3)
plt.bar(category_counts.index, category_counts.values)
plt.title("Stories by Category")
plt.xlabel("Category")
plt.ylabel("Number of Stories")
plt.subplot(2, 2, 4)
plt.barh(top_stories["title"], top_stories["score"])
plt.title("Top 10 Stories by Score")
plt.xlabel("Score")
plt.gca().invert_yaxis()
plt.suptitle("TrendPulse Dashboard", fontsize=24)
plt.tight_layout()
plt.savefig("outputs/dashboard.png")
plt.show()
print("Dashboard created successfully.")
