import requests
import pandas as pd
from datetime import datetime

APP_ID = "324684580"
APP_NAME = "Spotify"
CATEGORY = "Music"
COUNTRY = "us"

TARGET_REVIEWS = 100

rows = []

print("Collecting Apple App Store reviews...")

# Apple customer review feed is paginated.
# Each page generally contains up to around 50 reviews.
page = 1

while len(rows) < TARGET_REVIEWS:

    url = (
        f"https://itunes.apple.com/{COUNTRY}/rss/"
        f"customerreviews/page={page}/"
        f"id={APP_ID}/sortby=mostrecent/json"
    )

    response = requests.get(
        url,
        timeout=15
    )

    print(
        f"Page {page} | "
        f"Status: {response.status_code}"
    )

    if response.status_code != 200:
        print("Request failed.")
        break

    data = response.json()

    entries = (
        data.get("feed", {})
        .get("entry", [])
    )

    if not entries:
        print("No additional reviews returned.")
        break

    collection_time = datetime.now()

    for review in entries:

        # Stop after reaching target
        if len(rows) >= TARGET_REVIEWS:
            break

        rows.append({
            "platform": "Apple App Store",
            "app_name": APP_NAME,
            "app_id": APP_ID,
            "category": CATEGORY,

            "review_id": (
                review.get("id", {})
                .get("label")
            ),

            "review_title": (
                review.get("title", {})
                .get("label")
            ),

            "review_text": (
                review.get("content", {})
                .get("label")
            ),

            "rating": (
                review.get("im:rating", {})
                .get("label")
            ),

            "review_date": (
                review.get("updated", {})
                .get("label")
            ),

            "app_version": (
                review.get("im:version", {})
                .get("label")
            ),

            "reviewer_name": (
                review.get("author", {})
                .get("name", {})
                .get("label")
            ),

            "helpful_count": (
                review.get("im:voteCount", {})
                .get("label")
            ),

            "collection_timestamp": collection_time
        })

    print(
        f"Reviews collected so far: {len(rows)}"
    )

    page += 1


# --------------------------------------------------
# Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(rows)

# Convert numeric fields
if "rating" in df.columns:
    df["rating"] = pd.to_numeric(
        df["rating"],
        errors="coerce"
    )

if "helpful_count" in df.columns:
    df["helpful_count"] = pd.to_numeric(
        df["helpful_count"],
        errors="coerce"
    )


# --------------------------------------------------
# Output
# --------------------------------------------------

print("\nCollection complete.")

print("\nReviews collected:")
print(len(df))

print("\nColumns:")
print(df.columns.tolist())

print("\nFirst 5 rows:")
print(df.head())

print("\nMissing values:")
print(df.isnull().sum())

print("\nDuplicate review IDs:")
print(df["review_id"].duplicated().sum())

print("\nDuplicate review text:")
print(df["review_text"].duplicated().sum())

print("\nRating distribution:")
print(
    df["rating"]
    .value_counts()
    .sort_index()
)


# --------------------------------------------------
# Review length
# --------------------------------------------------

df["review_length"] = (
    df["review_text"]
    .fillna("")
    .str.len()
)

print("\nReview length summary:")
print(
    df["review_length"]
    .describe()
)


# --------------------------------------------------
# Date range
# --------------------------------------------------

df["review_date"] = pd.to_datetime(
    df["review_date"],
    errors="coerce",
    utc=True
)

print("\nDate range:")

print(
    "Earliest:",
    df["review_date"].min()
)

print(
    "Latest:",
    df["review_date"].max()
)


# --------------------------------------------------
# Save raw data
# --------------------------------------------------

output_path = "data/raw/apple_store_test.csv"

df.drop(
    columns=["review_length"]
).to_csv(
    output_path,
    index=False
)

print(
    f"\nSaved to: {output_path}"
)
