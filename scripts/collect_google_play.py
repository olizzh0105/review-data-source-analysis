from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime

APP_ID = "com.spotify.music"
APP_NAME = "Spotify"
CATEGORY = "Music"

TARGET_REVIEWS = 100

print("Collecting Google Play reviews...")

review_data, continuation_token = reviews(
    APP_ID,
    lang="en",
    country="us",
    sort=Sort.NEWEST,
    count=TARGET_REVIEWS
)

rows = []

for review in review_data:

    rows.append({
        "platform": "Google Play",
        "app_name": APP_NAME,
        "app_id": APP_ID,
        "category": CATEGORY,

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


df = pd.DataFrame(rows)

print("\nCollection complete.")
print("Reviews collected:", len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())


output_path = "data/raw/google_play_test.csv"

df.to_csv(
    output_path,
    index=False
)

print(f"\nSaved to: {output_path}")
