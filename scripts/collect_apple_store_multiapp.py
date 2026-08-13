import requests
import pandas as pd
from datetime import datetime
import time

apps = [
    {
        "app_name": "Spotify",
        "app_id": "324684580",
        "category": "Music"
    },
    {
        "app_name": "Uber",
        "app_id": "368677368",
        "category": "Transportation"
    },
    {
        "app_name": "Reddit",
        "app_id": "1064216828",
        "category": "Social / News"
    },
    {
        "app_name": "Duolingo",
        "app_id": "570060128",
        "category": "Education"
    }
]

COUNTRY = "us"
TARGET_REVIEWS_PER_APP = 100

all_rows = []

for app in apps:

    print("\n" + "=" * 60)
    print(f"Collecting {app['app_name']}")
    print("=" * 60)

    app_rows = []
    page = 1

    while len(app_rows) < TARGET_REVIEWS_PER_APP:

        url = (
            f"https://itunes.apple.com/{COUNTRY}/rss/"
            f"customerreviews/page={page}/"
            f"id={app['app_id']}/sortby=mostrecent/json"
        )

        try:
            response = requests.get(
                url,
                timeout=15
            )
        except Exception as e:
            print(
                f"Request error for {app['app_name']}: {e}"
            )
            break

        print(
            f"{app['app_name']} | "
            f"Page {page} | "
            f"Status: {response.status_code}"
        )

        if response.status_code != 200:
            print("Request failed.")
            break

        try:
            data = response.json()
        except Exception as e:
            print(f"JSON parsing error: {e}")
            break

        entries = (
            data.get("feed", {})
            .get("entry", [])
        )

        if not entries:
            print(
                f"No additional reviews returned for "
                f"{app['app_name']}."
            )
            break

        collection_time = datetime.now()

        for review in entries:

            if len(app_rows) >= TARGET_REVIEWS_PER_APP:
                break

            app_rows.append({
                "platform": "Apple App Store",
                "app_name": app["app_name"],
                "app_id": app["app_id"],
                "category": app["category"],

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
            f"{app['app_name']}: "
            f"{len(app_rows)} / "
            f"{TARGET_REVIEWS_PER_APP} reviews collected"
        )

        page += 1

        time.sleep(0.5)

    all_rows.extend(app_rows)

    print(
        f"Finished {app['app_name']}: "
        f"{len(app_rows)} reviews"
    )


# --------------------------------------------------
# Create DataFrame
# --------------------------------------------------

df = pd.DataFrame(all_rows)

df["rating"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

df["helpful_count"] = pd.to_numeric(
    df["helpful_count"],
    errors="coerce"
)

df["review_date"] = pd.to_datetime(
    df["review_date"],
    errors="coerce",
    utc=True
)


# --------------------------------------------------
# Validation
# --------------------------------------------------

print("\n" + "=" * 60)
print("APPLE MULTI-APP TEST SUMMARY")
print("=" * 60)

print("\nTotal reviews:")
print(len(df))

print("\nReviews by app:")
print(
    df["app_name"]
    .value_counts()
)

print("\nMissing values:")
print(
    df.isnull()
    .sum()
)

print("\nDuplicate review IDs:")
print(
    df["review_id"]
    .duplicated()
    .sum()
)

print("\nDuplicate review text:")
print(
    df["review_text"]
    .duplicated()
    .sum()
)

print("\nRating distribution by app:")
print(
    pd.crosstab(
        df["app_name"],
        df["rating"]
    )
)

df["review_length"] = (
    df["review_text"]
    .fillna("")
    .str.len()
)

print("\nReview length by app:")
print(
    df.groupby(
        "app_name"
    )["review_length"]
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


# --------------------------------------------------
# Save raw test data
# --------------------------------------------------

output_path = "data/raw/apple_store_4app_test.csv"

df.drop(
    columns=["review_length"]
).to_csv(
    output_path,
    index=False
)

print(f"\nSaved to: {output_path}")