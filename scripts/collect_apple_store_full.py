import requests
import pandas as pd
from datetime import datetime
import time


# --------------------------------------------------
# Configuration
# --------------------------------------------------

apps = [
    # Music & Audio
    {
        "app_name": "Spotify",
        "app_id": "324684580",
        "category": "Music & Audio"
    },
    {
        "app_name": "YouTube Music",
        "app_id": "1017492454",
        "category": "Music & Audio"
    },
    {
        "app_name": "SoundCloud",
        "app_id": "336353151",
        "category": "Music & Audio"
    },
    {
        "app_name": "Pandora",
        "app_id": "284035177",
        "category": "Music & Audio"
    },

    # Travel & Mobility
    {
        "app_name": "Uber",
        "app_id": "368677368",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Lyft",
        "app_id": "529379082",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Airbnb",
        "app_id": "401626263",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Booking.com",
        "app_id": "367003839",
        "category": "Travel & Mobility"
    },

    # Social & Community
    {
        "app_name": "Reddit",
        "app_id": "1064216828",
        "category": "Social & Community"
    },
    {
        "app_name": "TikTok",
        "app_id": "835599320",
        "category": "Social & Community"
    },
    {
        "app_name": "Pinterest",
        "app_id": "429047995",
        "category": "Social & Community"
    },
    {
        "app_name": "Discord",
        "app_id": "985746746",
        "category": "Social & Community"
    },

    # Education
    {
        "app_name": "Duolingo",
        "app_id": "570060128",
        "category": "Education"
    },
    {
        "app_name": "Khan Academy",
        "app_id": "469863705",
        "category": "Education"
    },
    {
        "app_name": "Quizlet",
        "app_id": "546473125",
        "category": "Education"
    },
    {
        "app_name": "Coursera",
        "app_id": "736535961",
        "category": "Education"
    },

    # Finance
    {
        "app_name": "PayPal",
        "app_id": "283646709",
        "category": "Finance"
    },
    {
        "app_name": "Venmo",
        "app_id": "351727428",
        "category": "Finance"
    },
    {
        "app_name": "Cash App",
        "app_id": "711923939",
        "category": "Finance"
    },
    {
        "app_name": "Robinhood",
        "app_id": "938003185",
        "category": "Finance"
    },

    # Productivity & Cloud
    {
        "app_name": "Notion",
        "app_id": "1232780281",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Dropbox",
        "app_id": "327630330",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Slack",
        "app_id": "618783545",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Microsoft OneDrive",
        "app_id": "477537958",
        "category": "Productivity & Cloud"
    }
]

COUNTRY = "us"
MAX_PAGES = 10

all_rows = []


# --------------------------------------------------
# Collection
# --------------------------------------------------

for app in apps:

    print("\n" + "=" * 60)
    print(f"Collecting {app['app_name']}")
    print("=" * 60)

    app_rows = []

    for page in range(1, MAX_PAGES + 1):

        url = (
            f"https://itunes.apple.com/{COUNTRY}/rss/"
            f"customerreviews/page={page}/"
            f"id={app['app_id']}/sortby=mostrecent/json"
        )

        try:
            response = requests.get(
                url,
                timeout=20
            )

        except Exception as e:
            print(
                f"Request error on page {page}: {e}"
            )
            break

        print(
            f"{app['app_name']} | "
            f"Page {page} | "
            f"Status: {response.status_code}"
        )

        if response.status_code != 200:
            print(
                f"Stopped {app['app_name']} "
                f"at page {page}."
            )
            break

        try:
            data = response.json()

        except Exception as e:
            print(
                f"JSON error on page {page}: {e}"
            )
            break

        entries = (
            data.get("feed", {})
            .get("entry", [])
        )

        if not entries:
            print(
                f"No reviews returned on page {page}."
            )
            break

        collection_time = datetime.now()

        for review in entries:

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

                "source_page": page,

                "collection_timestamp": collection_time
            })

        print(
            f"{app['app_name']}: "
            f"{len(app_rows)} raw reviews collected so far"
        )

        time.sleep(0.5)


    # Add this app to combined dataset
    all_rows.extend(app_rows)

    app_df = pd.DataFrame(app_rows)

    if not app_df.empty:

        unique_ids = app_df["review_id"].nunique()

        duplicate_ids = (
            app_df["review_id"]
            .duplicated()
            .sum()
        )

        print(
            f"\nFinished {app['app_name']}: "
            f"{len(app_df)} raw rows | "
            f"{unique_ids} unique IDs | "
            f"{duplicate_ids} duplicate IDs"
        )

    else:
        print(
            f"\nFinished {app['app_name']}: "
            "0 reviews collected"
        )


    # Save progress after every app
    progress_df = pd.DataFrame(all_rows)

    progress_df.to_csv(
        "data/raw/apple_store_reviews_progress.csv",
        index=False
    )

    print("Progress saved.")


# --------------------------------------------------
# Final Dataset
# --------------------------------------------------

df = pd.DataFrame(all_rows)

output_path = "data/raw/apple_store_reviews.csv"

df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# Validation Summary
# --------------------------------------------------

print("\n\n" + "=" * 60)
print("APPLE APP STORE COLLECTION SUMMARY")
print("=" * 60)

print("\nTotal raw rows:")
print(len(df))


print("\nRaw rows by app:")
print(
    df["app_name"]
    .value_counts()
    .sort_index()
)


print("\nUnique review IDs by app:")
print(
    df.groupby("app_name")[
        "review_id"
    ]
    .nunique()
    .sort_index()
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


print("\nMissing values:")
print(
    df.isnull()
    .sum()
)


# --------------------------------------------------
# Rating
# --------------------------------------------------

df["rating_numeric"] = pd.to_numeric(
    df["rating"],
    errors="coerce"
)

print("\nRating distribution by app:")

print(
    pd.crosstab(
        df["app_name"],
        df["rating_numeric"]
    )
)


# --------------------------------------------------
# Review Length
# --------------------------------------------------

df["review_length"] = (
    df["review_text"]
    .fillna("")
    .str.len()
)

print("\nReview length by app:")

print(
    df.groupby("app_name")[
        "review_length"
    ]
    .describe()
)


# --------------------------------------------------
# Date Coverage
# --------------------------------------------------

df["review_date_parsed"] = pd.to_datetime(
    df["review_date"],
    errors="coerce",
    utc=True
)

print("\nDate range by app:")

for app_name, group in df.groupby("app_name"):

    earliest = group[
        "review_date_parsed"
    ].min()

    latest = group[
        "review_date_parsed"
    ].max()

    print(
        f"{app_name}"
        f" | Earliest: {earliest}"
        f" | Latest: {latest}"
    )


# --------------------------------------------------
# Duplicate Page Check
# --------------------------------------------------

duplicate_rows = df[
    df["review_id"]
    .duplicated(keep=False)
].sort_values(
    ["app_name", "review_id", "source_page"]
)

print("\nPagination duplicate examples:")

if duplicate_rows.empty:

    print("No duplicate review IDs found.")

else:

    print(
        duplicate_rows[
            [
                "app_name",
                "review_id",
                "source_page",
                "review_date"
            ]
        ]
        .head(20)
        .to_string(index=False)
    )


print("\nFinal raw dataset saved to:")
print(output_path)
