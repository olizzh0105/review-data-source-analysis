import requests
import pandas as pd
from datetime import datetime
import time
import os
import shutil


# ==================================================
# Configuration
# ==================================================

apps = [

    # --------------------------------------------------
    # Music & Audio
    # --------------------------------------------------
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
    {
        "app_name": "Shazam",
        "app_id": "284993459",
        "category": "Music & Audio"
    },

    # --------------------------------------------------
    # Travel & Mobility
    # --------------------------------------------------
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
    {
        "app_name": "Waze",
        "app_id": "323229106",
        "category": "Travel & Mobility"
    },

    # --------------------------------------------------
    # Social & Community
    # --------------------------------------------------
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
    {
        "app_name": "Instagram",
        "app_id": "389801252",
        "category": "Social & Community"
    },

    # --------------------------------------------------
    # Education
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Finance
    # --------------------------------------------------
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

    # --------------------------------------------------
    # Productivity & Cloud
    # --------------------------------------------------
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
    },
    {
        "app_name": "Google Drive",
        "app_id": "507874739",
        "category": "Productivity & Cloud"
    }
]


COUNTRY = "us"
MAX_PAGES = 10
REQUEST_DELAY = 0.5

OUTPUT_PATH = "data/raw/apple_store_reviews.csv"
PROGRESS_PATH = "data/raw/apple_store_reviews_progress.csv"
SUMMARY_PATH = "data/raw/apple_store_collection_summary.csv"

all_rows = []
collection_summary = []


# ==================================================
# Backup existing final dataset
# ==================================================

if os.path.exists(OUTPUT_PATH):

    os.makedirs(
        "data/raw/archive",
        exist_ok=True
    )

    backup_timestamp = datetime.now().strftime(
        "%Y%m%d_%H%M%S"
    )

    backup_path = (
        "data/raw/archive/"
        f"apple_store_reviews_{backup_timestamp}.csv"
    )

    shutil.copy2(
        OUTPUT_PATH,
        backup_path
    )

    print(
        f"Existing Apple dataset backed up to:\n"
        f"{backup_path}\n"
    )


# ==================================================
# HTTP Session
# ==================================================

session = requests.Session()

session.headers.update({
    "User-Agent": (
        "Mozilla/5.0 "
        "(compatible; review-data-source-assessment)"
    )
})


# ==================================================
# Collection
# ==================================================

for app in apps:

    print("\n" + "=" * 60)
    print(f"Collecting {app['app_name']}")
    print("=" * 60)

    app_rows = []
    pages_collected = 0

    for page in range(1, MAX_PAGES + 1):

        url = (
            f"https://itunes.apple.com/{COUNTRY}/rss/"
            f"customerreviews/page={page}/"
            f"id={app['app_id']}/"
            f"sortby=mostrecent/json"
        )

        try:

            response = session.get(
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
                f"JSON parsing error on page "
                f"{page}: {e}"
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


        pages_collected += 1

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

                "collection_timestamp": (
                    collection_time
                )
            })


        print(
            f"{app['app_name']}: "
            f"{len(app_rows)} raw reviews "
            f"collected so far"
        )


        time.sleep(REQUEST_DELAY)


    # ==================================================
    # Per-app summary
    # ==================================================

    if app_rows:

        app_df = pd.DataFrame(app_rows)

        raw_rows = len(app_df)

        unique_ids = (
            app_df["review_id"]
            .nunique()
        )

        duplicate_ids = (
            app_df["review_id"]
            .duplicated()
            .sum()
        )


        review_dates = pd.to_datetime(
            app_df["review_date"],
            errors="coerce",
            utc=True
        )


        earliest_date = (
            review_dates.min()
        )

        latest_date = (
            review_dates.max()
        )


        print(
            f"\nFinished {app['app_name']}: "
            f"{raw_rows} raw rows | "
            f"{unique_ids} unique IDs | "
            f"{duplicate_ids} duplicate IDs"
        )


    else:

        raw_rows = 0
        unique_ids = 0
        duplicate_ids = 0
        earliest_date = None
        latest_date = None

        print(
            f"\nFinished {app['app_name']}: "
            f"0 reviews collected"
        )


    collection_summary.append({

        "app_name": app["app_name"],

        "app_id": app["app_id"],

        "category": app["category"],

        "pages_collected": pages_collected,

        "raw_rows": raw_rows,

        "unique_review_ids": unique_ids,

        "duplicate_review_ids": duplicate_ids,

        "earliest_review_date": earliest_date,

        "latest_review_date": latest_date
    })


    all_rows.extend(app_rows)


    # ==================================================
    # Save progress after every app
    # ==================================================

    progress_df = pd.DataFrame(
        all_rows
    )

    progress_df.to_csv(
        PROGRESS_PATH,
        index=False
    )


    summary_df = pd.DataFrame(
        collection_summary
    )

    summary_df.to_csv(
        SUMMARY_PATH,
        index=False
    )


    print("Progress saved.")


# ==================================================
# Final raw dataset
# ==================================================

df = pd.DataFrame(
    all_rows
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


# ==================================================
# Final collection summary
# ==================================================

summary_df = pd.DataFrame(
    collection_summary
)

summary_df.to_csv(
    SUMMARY_PATH,
    index=False
)


print("\n\n" + "=" * 70)
print("APPLE APP STORE COLLECTION SUMMARY")
print("=" * 70)


print("\nTotal apps attempted:")
print(len(apps))


print("\nApps with reviews:")
print(
    (summary_df["raw_rows"] > 0).sum()
)


print("\nApps with zero reviews:")
print(
    (summary_df["raw_rows"] == 0).sum()
)


print("\nTotal raw rows:")
print(len(df))


print("\nTotal unique review IDs:")
print(
    df["review_id"].nunique()
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


# ==================================================
# Raw rows by app
# ==================================================

print("\nRaw rows by app:")

print(
    summary_df[
        [
            "app_name",
            "raw_rows"
        ]
    ]
    .sort_values(
        "raw_rows",
        ascending=False
    )
    .to_string(index=False)
)


# ==================================================
# Unique IDs by app
# ==================================================

print("\nUnique review IDs by app:")

print(
    summary_df[
        [
            "app_name",
            "unique_review_ids"
        ]
    ]
    .sort_values(
        "unique_review_ids",
        ascending=False
    )
    .to_string(index=False)
)


# ==================================================
# Missing values
# ==================================================

print("\nMissing values:")

print(
    df.isnull()
    .sum()
)


# ==================================================
# Rating
# ==================================================

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


# ==================================================
# Review length
# ==================================================

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


# ==================================================
# Date coverage
# ==================================================

df["review_date_parsed"] = pd.to_datetime(
    df["review_date"],
    errors="coerce",
    utc=True
)


print("\nDate range by app:")

for app_name, group in df.groupby(
    "app_name"
):

    earliest = (
        group["review_date_parsed"]
        .min()
    )

    latest = (
        group["review_date_parsed"]
        .max()
    )

    print(
        f"{app_name}"
        f" | Earliest: {earliest}"
        f" | Latest: {latest}"
    )


# ==================================================
# Pagination duplicate examples
# ==================================================

duplicate_rows = df[
    df["review_id"]
    .duplicated(
        keep=False
    )
].sort_values(
    [
        "app_name",
        "review_id",
        "source_page"
    ]
)


print("\nPagination duplicate examples:")


if duplicate_rows.empty:

    print(
        "No duplicate review IDs found."
    )

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
        .head(30)
        .to_string(
            index=False
        )
    )


# ==================================================
# Target check
# ==================================================

print("\n" + "=" * 70)
print("TARGET CHECK")
print("=" * 70)


if len(df) >= 10000:

    print(
        f"SUCCESS: {len(df)} raw reviews collected."
    )

    print(
        "Apple dataset is within the "
        "target range of 10,000–20,000 reviews."
    )

else:

    remaining = 10000 - len(df)

    print(
        f"Current total: {len(df)} reviews."
    )

    print(
        f"Approximately {remaining} additional "
        f"reviews are needed to reach 10,000."
    )


print("\nFinal raw dataset:")
print(OUTPUT_PATH)

print("\nCollection summary:")
print(SUMMARY_PATH)