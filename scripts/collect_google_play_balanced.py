from google_play_scraper import reviews, Sort
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
        "app_id": "com.spotify.music",
        "category": "Music & Audio"
    },
    {
        "app_name": "YouTube Music",
        "app_id": "com.google.android.apps.youtube.music",
        "category": "Music & Audio"
    },
    {
        "app_name": "SoundCloud",
        "app_id": "com.soundcloud.android",
        "category": "Music & Audio"
    },
    {
        "app_name": "Pandora",
        "app_id": "com.pandora.android",
        "category": "Music & Audio"
    },
    {
        "app_name": "Shazam",
        "app_id": "com.shazam.android",
        "category": "Music & Audio"
    },

    # --------------------------------------------------
    # Travel & Mobility
    # --------------------------------------------------
    {
        "app_name": "Uber",
        "app_id": "com.ubercab",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Lyft",
        "app_id": "me.lyft.android",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Airbnb",
        "app_id": "com.airbnb.android",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Booking.com",
        "app_id": "com.booking",
        "category": "Travel & Mobility"
    },
    {
        "app_name": "Waze",
        "app_id": "com.waze",
        "category": "Travel & Mobility"
    },

    # --------------------------------------------------
    # Social & Community
    # --------------------------------------------------
    {
        "app_name": "Reddit",
        "app_id": "com.reddit.frontpage",
        "category": "Social & Community"
    },
    {
        "app_name": "TikTok",
        "app_id": "com.zhiliaoapp.musically",
        "category": "Social & Community"
    },
    {
        "app_name": "Pinterest",
        "app_id": "com.pinterest",
        "category": "Social & Community"
    },
    {
        "app_name": "Discord",
        "app_id": "com.discord",
        "category": "Social & Community"
    },
    {
        "app_name": "Instagram",
        "app_id": "com.instagram.android",
        "category": "Social & Community"
    },

    # --------------------------------------------------
    # Education
    # --------------------------------------------------
    {
        "app_name": "Duolingo",
        "app_id": "com.duolingo",
        "category": "Education"
    },
    {
        "app_name": "Khan Academy",
        "app_id": "org.khanacademy.android",
        "category": "Education"
    },
    {
        "app_name": "Quizlet",
        "app_id": "com.quizlet.quizletandroid",
        "category": "Education"
    },
    {
        "app_name": "Coursera",
        "app_id": "org.coursera.android",
        "category": "Education"
    },

    # --------------------------------------------------
    # Finance
    # --------------------------------------------------
    {
        "app_name": "PayPal",
        "app_id": "com.paypal.android.p2pmobile",
        "category": "Finance"
    },
    {
        "app_name": "Venmo",
        "app_id": "com.venmo",
        "category": "Finance"
    },
    {
        "app_name": "Cash App",
        "app_id": "com.squareup.cash",
        "category": "Finance"
    },
    {
        "app_name": "Robinhood",
        "app_id": "com.robinhood.android",
        "category": "Finance"
    },

    # --------------------------------------------------
    # Productivity & Cloud
    # --------------------------------------------------
    {
        "app_name": "Notion",
        "app_id": "notion.id",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Dropbox",
        "app_id": "com.dropbox.android",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Slack",
        "app_id": "com.Slack",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Microsoft OneDrive",
        "app_id": "com.microsoft.skydrive",
        "category": "Productivity & Cloud"
    },
    {
        "app_name": "Google Drive",
        "app_id": "com.google.android.apps.docs",
        "category": "Productivity & Cloud"
    }
]


TARGET_UNIQUE_REVIEWS_PER_APP = 500

BATCH_SIZE = 200

LANGUAGE = "en"
COUNTRY = "us"

REQUEST_DELAY = 0.5


OUTPUT_PATH = (
    "data/raw/google_play_balanced_reviews.csv"
)

PROGRESS_PATH = (
    "data/raw/google_play_balanced_reviews_progress.csv"
)

SUMMARY_PATH = (
    "data/raw/google_play_balanced_collection_summary.csv"
)


all_rows = []
collection_summary = []


# ==================================================
# Backup previous balanced dataset
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
        f"google_play_balanced_reviews_"
        f"{backup_timestamp}.csv"
    )

    shutil.copy2(
        OUTPUT_PATH,
        backup_path
    )

    print(
        f"Existing balanced Google Play dataset "
        f"backed up to:\n{backup_path}\n"
    )


# ==================================================
# Collection
# ==================================================

for app in apps:

    print("\n" + "=" * 70)
    print(f"Collecting {app['app_name']}")
    print("=" * 70)

    app_rows = []

    unique_review_ids = set()

    continuation_token = None

    batch_number = 0

    error_message = None


    while (
        len(unique_review_ids)
        < TARGET_UNIQUE_REVIEWS_PER_APP
    ):

        batch_number += 1

        remaining_unique = (
            TARGET_UNIQUE_REVIEWS_PER_APP
            - len(unique_review_ids)
        )

        current_batch_size = min(
            BATCH_SIZE,
            remaining_unique
        )


        try:

            review_data, continuation_token = reviews(
                app["app_id"],
                lang=LANGUAGE,
                country=COUNTRY,
                sort=Sort.NEWEST,
                count=current_batch_size,
                continuation_token=continuation_token
            )


        except Exception as e:

            error_message = str(e)

            print(
                f"Error collecting "
                f"{app['app_name']}: {e}"
            )

            break


        if not review_data:

            print(
                f"No additional reviews returned for "
                f"{app['app_name']}."
            )

            break


        collection_time = datetime.now()


        # ----------------------------------------------
        # Store raw results
        # ----------------------------------------------

        for review in review_data:

            review_id = review.get(
                "reviewId"
            )

            app_rows.append({

                "platform": "Google Play",

                "app_name": app["app_name"],

                "app_id": app["app_id"],

                "category": app["category"],

                "review_id": review_id,

                "review_text": review.get(
                    "content"
                ),

                "rating": review.get(
                    "score"
                ),

                "review_date": review.get(
                    "at"
                ),

                "app_version": review.get(
                    "reviewCreatedVersion"
                ),

                "developer_response": review.get(
                    "replyContent"
                ),

                "developer_response_date": review.get(
                    "repliedAt"
                ),

                "reviewer_name": review.get(
                    "userName"
                ),

                "helpful_count": review.get(
                    "thumbsUpCount"
                ),

                "source_batch": batch_number,

                "collection_timestamp": collection_time
            })


            if review_id is not None:

                unique_review_ids.add(
                    review_id
                )


        print(
            f"{app['app_name']} | "
            f"Batch {batch_number} | "
            f"Raw rows: {len(app_rows)} | "
            f"Unique IDs: {len(unique_review_ids)} / "
            f"{TARGET_UNIQUE_REVIEWS_PER_APP}"
        )


        # ----------------------------------------------
        # Stop if no continuation token
        # ----------------------------------------------

        if continuation_token is None:

            print(
                f"No continuation token returned for "
                f"{app['app_name']}."
            )

            break


        time.sleep(
            REQUEST_DELAY
        )


    # ==================================================
    # Per-app summary
    # ==================================================

    if app_rows:

        app_df = pd.DataFrame(
            app_rows
        )

        raw_rows = len(
            app_df
        )

        unique_ids = app_df[
            "review_id"
        ].nunique()

        duplicate_ids = (
            app_df["review_id"]
            .duplicated()
            .sum()
        )


        review_dates = pd.to_datetime(
            app_df["review_date"],
            errors="coerce"
        )


        earliest_date = (
            review_dates.min()
        )

        latest_date = (
            review_dates.max()
        )


        app_version_available = (
            app_df["app_version"]
            .notna()
            .mean()
        )


        developer_response_available = (
            app_df["developer_response"]
            .notna()
            .mean()
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

        app_version_available = None
        developer_response_available = None


        print(
            f"\nFinished {app['app_name']}: "
            f"0 reviews collected"
        )


    collection_summary.append({

        "app_name": app["app_name"],

        "app_id": app["app_id"],

        "category": app["category"],

        "batches_collected": batch_number,

        "raw_rows": raw_rows,

        "unique_review_ids": unique_ids,

        "duplicate_review_ids": duplicate_ids,

        "earliest_review_date": earliest_date,

        "latest_review_date": latest_date,

        "app_version_availability": (
            app_version_available
        ),

        "developer_response_availability": (
            developer_response_available
        ),

        "collection_error": error_message
    })


    all_rows.extend(
        app_rows
    )


    # ==================================================
    # Save progress after each app
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
# Save final raw dataset
# ==================================================

df = pd.DataFrame(
    all_rows
)

df.to_csv(
    OUTPUT_PATH,
    index=False
)


summary_df = pd.DataFrame(
    collection_summary
)

summary_df.to_csv(
    SUMMARY_PATH,
    index=False
)


# ==================================================
# Final Validation Summary
# ==================================================

print("\n\n" + "=" * 70)
print("GOOGLE PLAY BALANCED COLLECTION SUMMARY")
print("=" * 70)


print("\nTotal apps attempted:")
print(
    len(apps)
)


print("\nApps with reviews:")
print(
    (
        summary_df["raw_rows"]
        > 0
    ).sum()
)


print("\nApps with zero reviews:")
print(
    (
        summary_df["raw_rows"]
        == 0
    ).sum()
)


print("\nTotal raw rows:")
print(
    len(df)
)


print("\nTotal unique review IDs:")
print(
    df["review_id"]
    .nunique()
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
# Raw rows / unique IDs by app
# ==================================================

print("\nReviews by app:")

print(
    summary_df[
        [
            "app_name",
            "raw_rows",
            "unique_review_ids"
        ]
    ]
    .sort_values(
        "unique_review_ids",
        ascending=False
    )
    .to_string(
        index=False
    )
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
# Rating distributions
# ==================================================

print("\nRating distribution by app:")

print(
    pd.crosstab(
        df["app_name"],
        df["rating"]
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
    errors="coerce"
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
# Metadata availability
# ==================================================

print("\nApp version availability by app:")

print(
    df.groupby(
        "app_name"
    )["app_version"]
    .apply(
        lambda x: x.notna().mean()
    )
    .sort_values()
)


print("\nDeveloper response availability by app:")

print(
    df.groupby(
        "app_name"
    )["developer_response"]
    .apply(
        lambda x: x.notna().mean()
    )
    .sort_values()
)


# ==================================================
# Duplicate ID examples
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
        "source_batch"
    ]
)


print("\nDuplicate review ID examples:")


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
                "source_batch",
                "review_date"
            ]
        ]
        .head(30)
        .to_string(
            index=False
        )
    )


# ==================================================
# Collection errors
# ==================================================

errors = summary_df[
    summary_df[
        "collection_error"
    ].notna()
]


print("\nCollection errors:")


if errors.empty:

    print(
        "No collection errors."
    )

else:

    print(
        errors[
            [
                "app_name",
                "collection_error"
            ]
        ]
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


unique_total = (
    df["review_id"]
    .nunique()
)


if 10000 <= unique_total <= 20000:

    print(
        f"SUCCESS: "
        f"{unique_total} unique Google Play "
        f"reviews collected."
    )

    print(
        "Google Play balanced dataset is "
        "within the target range of "
        "10,000–20,000 reviews."
    )


elif unique_total < 10000:

    remaining = (
        10000
        - unique_total
    )

    print(
        f"Current unique total: "
        f"{unique_total}"
    )

    print(
        f"Approximately {remaining} "
        f"additional reviews are needed "
        f"to reach 10,000."
    )


else:

    print(
        f"Current unique total: "
        f"{unique_total}"
    )

    print(
        "Dataset exceeds the planned "
        "20,000-review upper range."
    )


print("\nFinal balanced raw dataset:")
print(
    OUTPUT_PATH
)

print("\nCollection summary:")
print(
    SUMMARY_PATH
)