import pandas as pd
import os


# ==================================================
# Paths
# ==================================================

APPLE_RAW = "data/raw/apple_store_reviews.csv"
GOOGLE_RAW = "data/raw/google_play_balanced_reviews.csv"

OUTPUT_DIR = "data/processed"

APPLE_OUTPUT = (
    "data/processed/apple_store_analysis.csv"
)

GOOGLE_OUTPUT = (
    "data/processed/google_play_analysis.csv"
)

COUNT_OUTPUT = (
    "data/processed/matched_sample_counts.csv"
)


# ==================================================
# Create processed folder
# ==================================================

os.makedirs(
    OUTPUT_DIR,
    exist_ok=True
)


# ==================================================
# Load raw datasets
# ==================================================

apple = pd.read_csv(
    APPLE_RAW
)

google = pd.read_csv(
    GOOGLE_RAW
)


print("Raw Apple rows:", len(apple))
print("Raw Google rows:", len(google))


# ==================================================
# Parse dates
# ==================================================

apple["review_date"] = pd.to_datetime(
    apple["review_date"],
    errors="coerce",
    utc=True
)

google["review_date"] = pd.to_datetime(
    google["review_date"],
    errors="coerce",
    utc=True
)


# ==================================================
# Remove duplicate review IDs
# from analysis datasets only
# ==================================================

apple_clean = (
    apple
    .sort_values(
        "review_date",
        ascending=False
    )
    .drop_duplicates(
        subset=["review_id"],
        keep="first"
    )
    .copy()
)


google_clean = (
    google
    .sort_values(
        "review_date",
        ascending=False
    )
    .drop_duplicates(
        subset=["review_id"],
        keep="first"
    )
    .copy()
)


print(
    "Apple unique rows:",
    len(apple_clean)
)

print(
    "Google unique rows:",
    len(google_clean)
)


# ==================================================
# Determine matched sample size
# for every app
# ==================================================

apple_counts = (
    apple_clean
    .groupby("app_name")
    .size()
)

google_counts = (
    google_clean
    .groupby("app_name")
    .size()
)


shared_apps = sorted(
    set(apple_counts.index)
    & set(google_counts.index)
)


sample_plan = []


for app in shared_apps:

    apple_available = (
        apple_counts[app]
    )

    google_available = (
        google_counts[app]
    )

    # Maximum planned sample per app = 500
    matched_count = min(
        500,
        apple_available,
        google_available
    )

    sample_plan.append({
        "app_name": app,
        "apple_available": apple_available,
        "google_available": google_available,
        "matched_count": matched_count
    })


sample_counts = pd.DataFrame(
    sample_plan
)


print("\nMatched sample counts:")
print(
    sample_counts.to_string(
        index=False
    )
)


# ==================================================
# Build Apple matched dataset
# ==================================================

apple_samples = []


for _, row in sample_counts.iterrows():

    app = row["app_name"]

    n = int(
        row["matched_count"]
    )

    sample = (
        apple_clean[
            apple_clean["app_name"] == app
        ]
        .sort_values(
            "review_date",
            ascending=False
        )
        .head(n)
    )

    apple_samples.append(
        sample
    )


apple_analysis = pd.concat(
    apple_samples,
    ignore_index=True
)


# ==================================================
# Build Google matched dataset
# ==================================================

google_samples = []


for _, row in sample_counts.iterrows():

    app = row["app_name"]

    n = int(
        row["matched_count"]
    )

    sample = (
        google_clean[
            google_clean["app_name"] == app
        ]
        .sort_values(
            "review_date",
            ascending=False
        )
        .head(n)
    )

    google_samples.append(
        sample
    )


google_analysis = pd.concat(
    google_samples,
    ignore_index=True
)


# ==================================================
# Save
# ==================================================

apple_analysis.to_csv(
    APPLE_OUTPUT,
    index=False
)

google_analysis.to_csv(
    GOOGLE_OUTPUT,
    index=False
)

sample_counts.to_csv(
    COUNT_OUTPUT,
    index=False
)


# ==================================================
# Validation
# ==================================================

print("\n" + "=" * 60)
print("BALANCED ANALYSIS DATASET SUMMARY")
print("=" * 60)


print("\nApple analysis rows:")
print(
    len(apple_analysis)
)


print("\nGoogle analysis rows:")
print(
    len(google_analysis)
)


print("\nApple rows by app:")
print(
    apple_analysis[
        "app_name"
    ].value_counts().sort_index()
)


print("\nGoogle rows by app:")
print(
    google_analysis[
        "app_name"
    ].value_counts().sort_index()
)


print("\nApple duplicate IDs:")
print(
    apple_analysis[
        "review_id"
    ].duplicated().sum()
)


print("\nGoogle duplicate IDs:")
print(
    google_analysis[
        "review_id"
    ].duplicated().sum()
)


print("\nSaved:")
print(APPLE_OUTPUT)
print(GOOGLE_OUTPUT)
print(COUNT_OUTPUT)