# Phase II Data Collection Plan

## Objective

The objective of Phase II is to collect substantially larger review datasets from both Google Play Store and Apple App Store and use the collected data for exploratory data analysis (EDA).

The target is approximately 10,000–20,000 reviews per platform.

The collection will include multiple applications across several categories. Where possible, the same applications will be included on both platforms to support later cross-platform comparisons.

---

## Sampling Strategy

A balanced multi-app sampling strategy will be used rather than collecting a large number of reviews from a single application.

The initial plan is to collect approximately 3,000 reviews per app from four applications on each platform.

This would produce approximately:

- Google Play Store: 12,000 reviews
- Apple App Store: 12,000 reviews
- Combined dataset: approximately 24,000 reviews

The same applications will be used across both platforms where possible.

This sampling approach is intended to support:

- Cross-app comparison
- Cross-category comparison
- Cross-platform comparison
- Rating distribution analysis
- Review-length analysis
- Time-based analysis
- Data-quality assessment

---

## Selected Apps

| Category | App | Google Play ID | Apple App Store ID | Target Reviews per Platform |
|---|---|---|---|---:|
| Music | Spotify | `com.spotify.music` | `324684580` | 3,000 |
| Transportation | Uber | `com.ubercab` | `368677368` | 3,000 |
| Social / News | Reddit | `com.reddit.frontpage` | `1064216828` | 3,000 |
| Education | Duolingo | `com.duolingo` | `570060128` | 3,000 |

### Sampling Rationale

These applications were selected because they represent different product categories and have substantial user-review activity.

Using the same applications on both Google Play Store and Apple App Store will allow later comparisons such as:

- Whether the same app receives different rating distributions across platforms
- Whether review length differs between Android and iOS users
- Whether users discuss different product issues across platforms
- Whether negative feedback patterns differ for the same application

---

## Target Review Counts

| Platform | Apps | Target per App | Approximate Total |
|---|---:|---:|---:|
| Google Play Store | 4 | 3,000 | 12,000 |
| Apple App Store | 4 | 3,000 | 12,000 |

The target counts may be adjusted depending on the number of reviews that can be consistently retrieved from each application.

The goal is to remain within the requested range of approximately 10,000–20,000 reviews per platform while maintaining reasonable balance across applications.

---

## Expected Fields

The collection process will initially attempt to capture the following fields where available:

### Core Fields

- `platform`
- `app_name`
- `app_id`
- `category`
- `review_id`
- `review_text`
- `rating`
- `review_date`
- `collection_timestamp`

### Additional Metadata

Where consistently available, additional fields may include:

- `app_version`
- `developer_response`
- `developer_response_date`
- `reviewer_name`
- `language`
- `helpful_count`

The final EDA will be based only on fields that are consistently observed in the collected data.

Any differences between expected fields and actually available fields will be documented.

---

## Collection Method

Separate collection scripts will be developed for the two platforms:

- `scripts/collect_google_play.py`
- `scripts/collect_apple_store.py`

Raw collected data will be stored separately by platform:

- `data/raw/google_play_reviews.csv`
- `data/raw/apple_reviews.csv`

The collection scripts should:

1. Iterate across the selected applications.
2. Retrieve multiple reviews for each application.
3. Capture available review fields.
4. Add platform, application, and category identifiers.
5. Combine reviews into a platform-level dataset.
6. Save the raw results without extensive transformation.

Cleaning and transformation will be performed separately during the EDA phase.

---

## Data Quality Considerations

The collected data will later be evaluated for:

- Missing values
- Duplicate review IDs
- Repeated review text
- Empty or very short reviews
- Rating distributions
- Review-length distributions
- Timestamp coverage
- Language distribution
- App-version availability
- Developer-response availability
- Differences in field availability across platforms
- Differences across apps and categories

Special attention will be given to identifying fields that were expected based on documentation but were not consistently available through the actual collection method.

---

## Planned EDA

After collection is complete, the analysis will examine:

1. Review counts by platform and app
2. Rating distributions
3. Review-text length
4. Low-information comments
5. Timestamp coverage
6. Missing-value patterns
7. Duplicate reviews
8. Language distribution
9. App-version availability
10. Developer-response availability
11. Differences across apps and categories
12. Cross-platform differences for the same apps
13. Relationships between ratings and review characteristics
14. Data-quality implications for future sentiment analysis

The majority of Phase II will focus on understanding and interpreting the collected datasets rather than only on the collection process.
