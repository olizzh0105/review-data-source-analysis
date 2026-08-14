# Phase II Data Collection Plan

## Objective

The objective of Phase II is to collect substantially larger review datasets from both Google Play Store and Apple App Store and use the collected data for exploratory data analysis (EDA).

The target is approximately 10,000–20,000 reviews per platform.

The collection will include multiple applications across several categories. Where possible, the same applications will be included on both platforms to support later cross-platform comparisons.

---

## Sampling Strategy

A balanced multi-app sampling strategy will be used rather than collecting a large number of reviews from a single application.

Based on practical pagination testing, the sampling strategy was revised to use a broader set of applications with up to approximately 500 unique reviews per app.

The revised design includes 24 applications across six study categories. The same applications will be included on both Google Play Store and Apple App Store to support balanced cross-platform comparisons.

This strategy targets approximately:

- Google Play Store: 12,000 reviews
- Apple App Store: 12,000 reviews
- Combined dataset: approximately 24,000 reviews

The revised approach reflects the observed pagination limit of the Apple App Store review feed while also improving cross-app and cross-category coverage.

The same applications will be used across both platforms to support direct cross-platform comparisons.

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
| Music & Audio | Spotify | `com.spotify.music` | `324684580` | Up to 500 |
| Music & Audio | YouTube Music | `com.google.android.apps.youtube.music` | `1017492454` | Up to 500 |
| Music & Audio | SoundCloud | `com.soundcloud.android` | `336353151` | Up to 500 |
| Music & Audio | Pandora | `com.pandora.android` | `284035177` | Up to 500 |
| Travel & Mobility | Uber | `com.ubercab` | `368677368` | Up to 500 |
| Travel & Mobility | Lyft | `me.lyft.android` | `529379082` | Up to 500 |
| Travel & Mobility | Airbnb | `com.airbnb.android` | `401626263` | Up to 500 |
| Travel & Mobility | Booking.com | `com.booking` | `367003839` | Up to 500 |
| Social & Community | Reddit | `com.reddit.frontpage` | `1064216828` | Up to 500 |
| Social & Community | TikTok | `com.zhiliaoapp.musically` | `835599320` | Up to 500 |
| Social & Community | Pinterest | `com.pinterest` | `429047995` | Up to 500 |
| Social & Community | Discord | `com.discord` | `985746746` | Up to 500 |
| Education | Duolingo | `com.duolingo` | `570060128` | Up to 500 |
| Education | Khan Academy | `org.khanacademy.android` | `469863705` | Up to 500 |
| Education | Quizlet | `com.quizlet.quizletandroid` | `546473125` | Up to 500 |
| Education | Coursera | `org.coursera.android` | `736535961` | Up to 500 |
| Finance | PayPal | `com.paypal.android.p2pmobile` | `283646709` | Up to 500 |
| Finance | Venmo | `com.venmo` | `351727428` | Up to 500 |
| Finance | Cash App | `com.squareup.cash` | `711923939` | Up to 500 |
| Finance | Robinhood | `com.robinhood.android` | `938003185` | Up to 500 |
| Productivity & Cloud | Notion | `notion.id` | `1232780281` | Up to 500 |
| Productivity & Cloud | Dropbox | `com.dropbox.android` | `327630330` | Up to 500 |
| Productivity & Cloud | Slack | `com.Slack` | `618783545` | Up to 500 |
| Productivity & Cloud | Microsoft OneDrive | `com.microsoft.skydrive` | `477537958` | Up to 500 |

### Sampling Rationale

These applications were selected because they represent different product categories and have substantial user-review activity. The broader 24-app design was adopted after practical testing showed that the Apple App Store review feed provided up to approximately 500 reviews per application through the tested pagination method.

Using the same applications on both Google Play Store and Apple App Store will allow later comparisons such as:

- Whether the same app receives different rating distributions across platforms
- Whether review length differs between Android and iOS users
- Whether users discuss different product issues across platforms
- Whether negative feedback patterns differ for the same application

---

## Target Review Counts

| Platform | Apps | Target per App | Approximate Total |
|---|---:|---:|---:|
| Google Play Store | 24 | Up to 500 | 12,000 |
| Apple App Store | 24 | Up to 500 | 12,000 |

Actual review counts may vary if fewer than 500 unique reviews are available through the collection method for a particular application.

The goal is to remain within the requested range of approximately 10,000–20,000 reviews per platform while maintaining broad coverage across applications and categories.

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

- `review_title`
- `app_version`
- `developer_response`
- `developer_response_date`
- `reviewer_name`
- `helpful_count`
- `source_page`

Language was considered during the planning stage but was not directly available as a review-level field in the initial collection outputs. Language-related analysis may therefore require separate detection during EDA rather than relying on source metadata.

---

## Collection Method

The final balanced collection will use platform-specific scripts:

- `scripts/collect_google_play_balanced.py`
- `scripts/collect_apple_store_full.py`

Earlier collection scripts are retained as validation and methodology-development steps:

- `scripts/collect_google_play.py`: single-app smoke test using Spotify
- `scripts/collect_google_play_multiapp.py`: four-app validation test
- `scripts/collect_google_play_full.py`: original four-app deep collection with approximately 3,000 reviews per app
- `scripts/collect_google_play_balanced.py`: revised balanced collection across 24 apps with up to 500 reviews per app
- `scripts/collect_apple_store.py`: single-app Apple App Store smoke test
- `scripts/collect_apple_store_multiapp.py`: four-app Apple App Store validation test
- `scripts/collect_apple_store_full.py`: final balanced Apple App Store collection across 24 apps with up to 500 reviews per app

Raw collected data will be stored separately by platform:

- `data/raw/google_play_reviews.csv`
- `data/raw/apple_store_reviews.csv`

Raw collected data will be preserved without deduplication. Duplicate review IDs identified during collection will be documented and handled separately during data processing and EDA.

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

Where applicable based on the fields actually available for each platform, the collected data will later be evaluated for:

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
