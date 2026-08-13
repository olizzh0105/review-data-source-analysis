from google_play_scraper import reviews, Sort
import pandas as pd
from datetime import datetime
import time

# --------------------------------------------------
# Configuration
# --------------------------------------------------

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

TARGET_REVIEWS_PER_APP = 3000

# Google Play returns reviews in batches.
BATCH_SIZE = 200

all_rows = []


# --------------------------------------------------
# Collection
# --------------------------------------------------

for app in apps:

    print("\n" + "=" * 60)
    print(f"Collecting {app['app_name']}")
    print("=" * 60)

    app_rows = []
    continuation_token = None

    while len(app_rows) < TARGET_REVIEWS_PER_APP:

        remaining = TARGET_REVIEWS_PER_APP - len(app_rows)

        current_batch_size = min(
            BATCH_SIZE,
            remaining
        )

        try:

            review_data, continuation_token = reviews(
                app["app_id"],
                lang="en",
                country="us",
                sort=Sort.NEWEST,
                count=current_batch_size,
                continuation_token=continuation_token
            )

        except Exception as e:

            print(
                f"Error collecting {app['app_name']}: {e}"
            )

            break

        # Stop if Google Play returns no more reviews
        if not review_data:

            print(
                f"No additional reviews returned for "
                f"{app['app_name']}."
            )

            break

        collection_time = datetime.now()

        for review in review_data:

            app_rows.append({
                "platform": "Google Play",
                "app_name": app["app_name"],
                "app_id": app["app_id"],
                "category": app["category"],

                "review_id": review.get("reviewId"),
                "review_text": review.get("content"),
                "rating": review.get("score"),
                "review_date": review.get("at"),

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

                "collection_timestamp": collection_time
            })

        print(
            f"{app['app_name']}: "
            f"{len(app_rows)} / "
            f"{TARGET_REVIEWS_PER_APP} reviews collected"
        )

        # Stop if there is no next page
        if continuation_token is None:
            print(
                f"No continuation token returned for "
                f"{app['app_name']}."
            )
            break

        # Small pause between batches
        time.sleep(0.5)


    # Keep only the requested number
    app_rows = app_rows[:TARGET_REVIEWS_PER_APP]

    all_rows.extend(app_rows)

    print(
        f"\nFinished {app['app_name']}: "
        f"{len(app_rows)} reviews"
    )

    # Save progress after every app
    progress_df = pd.DataFrame(all_rows)

    progress_df.to_csv(
        "data/raw/google_play_reviews_progress.csv",
        index=False
    )

    print("Progress saved.")


# --------------------------------------------------
# Final Dataset
# --------------------------------------------------

df = pd.DataFrame(all_rows)

output_path = "data/raw/google_play_reviews.csv"

df.to_csv(
    output_path,
    index=False
)


# --------------------------------------------------
# Validation Summary
# --------------------------------------------------

print("\n\n" + "=" * 60)
print("GOOGLE PLAY COLLECTION SUMMARY")
print("=" * 60)

print("\nTotal reviews collected:")
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
    df.groupby(
        "app_name"
    )["review_length"]
    .describe()
)


# --------------------------------------------------
# Date Coverage
# --------------------------------------------------

print("\nDate range by app:")

for app_name, group in df.groupby("app_name"):

    earliest = group["review_date"].min()
    latest = group["review_date"].max()

    print(
        f"{app_name}"
        f" | Earliest: {earliest}"
        f" | Latest: {latest}"
    )


# --------------------------------------------------
# Missing Metadata by App
# --------------------------------------------------

print("\nApp version availability:")

print(
    df.groupby("app_name")[
        "app_version"
    ]
    .apply(
        lambda x: x.notna().mean()
    )
)


print("\nDeveloper response availability:")

print(
    df.groupby("app_name")[
        "developer_response"
    ]
    .apply(
        lambda x: x.notna().mean()
    )
)


print("\nFinal dataset saved to:")
print(output_path)