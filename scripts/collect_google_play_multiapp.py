from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

apps = [
    {
        "app_name": "Spotify",
        "app_id": "com.spotify.music",
        "category": "Music"
    },
    {
        "app_name": "Uber",
        "app_id": "com.ubercab",
        "category": "Transportation"
    },
    {
        "app_name": "Reddit",
        "app_id": "com.reddit.frontpage",
        "category": "Social / News"
    },
    {
        "app_name": "Duolingo",
        "app_id": "com.duolingo",
        "category": "Education"
    }
]

TARGET_REVIEWS_PER_APP = 100

rows = []

for app in apps:

    print(f"\nCollecting {app['app_name']} reviews...")

    review_data, continuation_token = reviews(
        app["app_id"],
        lang="en",
        country="us",
        sort=Sort.NEWEST,
        count=TARGET_REVIEWS_PER_APP
    )

    for review in review_data:

        rows.append({
            "platform": "Google Play",
            "app_name": app["app_name"],
            "app_id": app["app_id"],
            "category": app["category"],
            "review_id": review.get("reviewId"),
            "review_text": review.get("content"),
            "rating": review.get("score"),
            "review_date": review.get("at"),
            "app_version": review.get("reviewCreatedVersion"),
            "developer_response": review.get("replyContent"),
            "developer_response_date": review.get("repliedAt"),
            "reviewer_name": review.get("userName"),
            "helpful_count": review.get("thumbsUpCount"),
            "collection_timestamp": datetime.now()
        })

    print(
        f"{app['app_name']}: "
        f"{len(review_data)} reviews collected"
    )

df = pd.DataFrame(rows)

print("\nTotal reviews collected:")
print(len(df))

print("\nReviews by app:")
print(df["app_name"].value_counts())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate review IDs:")
print(df["review_id"].duplicated().sum())

print("\nDuplicate review text:")
print(df["review_text"].duplicated().sum())

print("\nRating distribution by app:")
print(
    pd.crosstab(
        df["app_name"],
        df["rating"]
    )
)

df["review_length"] = df["review_text"].str.len()

print("\nReview length by app:")
print(
    df.groupby("app_name")["review_length"]
    .describe()
)

print("\nDate range by app:")

for app_name, group in df.groupby("app_name"):
    print(
        app_name,
        "| Earliest:",
        group["review_date"].min(),
        "| Latest:",
        group["review_date"].max()
    )

output_path = "data/raw/google_play_4app_test.csv"

df.drop(
    columns=["review_length"]
).to_csv(
    output_path,
    index=False
)

print(f"\nSaved to: {output_path}")