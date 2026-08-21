# Review Data Source Assessment and Cross-Platform Review Analysis

This project evaluates and analyzes user-review data sources for downstream sentiment and product analysis.

The project is organized into two phases:

- **Phase I – Data Source Assessment:** evaluates Amazon, Google Play Store, and Apple App Store from business, technical, and practical perspectives.
- **Phase II – Large-Scale Collection and Analysis:** builds matched Google Play Store and Apple App Store review datasets and conducts app-level, category-level, and cross-platform exploratory analysis.

Phase I identified Google Play Store as the strongest initial source for a recurring review-data workflow. Phase II expands the analysis by using both Google Play Store and Apple App Store in parallel to better understand differences in ratings, review quality, metadata availability, and user-feedback patterns.

> [!NOTE]
> **Phase I Recommendation: Google Play Store**
>
> Phase I recommended Google Play Store as the strongest initial source based on review richness, metadata availability, repeatability, extraction feasibility, and downstream analytical potential.
>
> Phase II extends the project by analyzing **Google Play Store and Apple App Store in parallel** using matched samples from the same applications.

---

## Outline

- [Overview](#overview)
- [Research Question](#research-question)
- [Evaluation Framework](#evaluation-framework)
- [Data Sources](#data-sources)
- [Practical Testing](#practical-testing)
- [Key Results](#key-results)
- [Phase II: Large-Scale Collection and Analysis](#phase-ii-large-scale-collection-and-analysis)
- [Phase II Dataset](#phase-ii-dataset)
- [Analysis Structure](#analysis-structure)
- [Preliminary Findings](#preliminary-findings)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Running the Project](#running-the-project)
- [Phase I Recommendation](#phase-i-recommendation)
- [Limitations](#limitations)
- [Next Steps](#next-steps)
- [Project Status](#project-status)

---

## Overview

The purpose of this project is to assess potential sources of user-generated review data for an AI-powered sentiment analytics workflow.

Three platforms were evaluated:

- **Amazon**
- **Google Play Store**
- **Apple App Store**

The project focuses on determining whether each source offers:

- Relevant and sufficiently rich user feedback
- Useful metadata for downstream analysis
- Publicly accessible review information
- A reasonably stable and repeatable collection process
- Suitable structure for future automated ingestion

The full business and technical analysis is available in [`assessment.md`](./assessment.md).

---

## Research Question

**Which of Amazon, Google Play Store, and Apple App Store is the most suitable source for building a recurring review-data ingestion workflow for downstream sentiment analysis?**

---

## Evaluation Framework

The three platforms were evaluated from two main perspectives.

### Business Perspective

| Criterion | Description |
|---|---|
| Review Relevance | How well reviews reflect actual user experiences |
| Review Richness | Level of detail and informational value in review content |
| Product Coverage | Range of products, services, or applications represented |
| Metadata Richness | Availability of ratings, dates, versions, and related metadata |
| Analytical Potential | Types of downstream analysis supported |
| Limitations | Potential biases or weaknesses in the data |

### Technical / Practical Perspective

| Criterion | Description |
|---|---|
| Public Accessibility | Whether review-related data can be accessed without login |
| Data Structure | Consistency and usability of returned data |
| Repeatability | Whether collection appears reproducible across repeated requests |
| Restrictions | API, authorization, or public-web collection limitations |
| Recurring Workflow Suitability | Suitability for ongoing automated ingestion |

---
## Data Sources

The assessment focuses on publicly visible customer review data from three platforms.

| Platform | Data Type | Representative Page Used for Testing |
|---|---|---|
| Amazon | Product reviews | [Amazon Echo Dot (5th Gen)](https://www.amazon.com/Amazon-vibrant-helpful-routines-Charcoal/dp/B09B8V1LZ3) |
| Google Play Store | Mobile app reviews | [Spotify - Google Play](https://play.google.com/store/apps/details?id=com.spotify.music) |
| Apple App Store | Mobile app reviews | [Spotify - Apple App Store](https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580) |

The Google Play Store and Apple App Store tests use Spotify as a representative application to make the comparison between the two app platforms more consistent.

Amazon uses a representative consumer product page because Amazon primarily provides product-level rather than application-level customer reviews.

These pages were used only for lightweight feasibility testing. The project does not assume that results from a single page represent all pages available on each platform.

### Official Documentation Referenced

The technical assessment also considers official platform documentation related to programmatic review access:

- [Amazon Creators API Documentation](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/introduction)
- [Amazon Creators API Resources](https://affiliate-program.amazon.com/creatorsapi/docs/en-us/api-reference/resources)

- [Google Play Developer API](https://developers.google.com/android-publisher)
- [Google Play Reviews Resource](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews)
- [Google Play Reviews List Method](https://developers.google.com/android-publisher/api-ref/rest/v3/reviews/list)

- [Apple App Store Connect API](https://developer.apple.com/documentation/appstoreconnectapi)
- [Apple Customer Reviews Documentation](https://developer.apple.com/documentation/appstoreconnectapi/customer-reviews)
- [Apple Customer Reviews API Endpoint](https://developer.apple.com/documentation/appstoreconnectapi/get-v1-apps-_id_-customerreviews)

---

## Practical Testing

In addition to secondary research, several lightweight Python tests were conducted.

The purpose was **not to build a production scraper**, but to compare the initial technical feasibility of the three platforms.

### 1. Basic Programmatic Accessibility Test

Python `requests` was used to retrieve one representative public page from each platform.

| Platform | HTTP Status | Initial Result |
|---|---:|---|
| Amazon | 200 | Successfully retrieved |
| Google Play Store | 200 | Successfully retrieved |
| Apple App Store | 200 | Successfully retrieved |

All three platforms were initially accessible through basic HTTP requests.

---

### 2. Review Field Availability Test

Returned page content was checked for review-related terms such as:

- `review`
- `rating`
- `date`
- `version`
- `author`
- `helpful`

Google Play Store exposed the broadest range of review-related information in this lightweight test.

---

### 3. Repeatability Test

Repeated HTTP requests produced different results across platforms.

Google Play Store and Apple App Store returned relatively consistent responses.

Amazon showed substantially different responses between runs, including one response that returned a much smaller page despite still returning HTTP status code `200`.

This suggests that successful HTTP status alone may not guarantee consistent retrieval of the expected Amazon product page.

---

### 4. Small Review Extraction Test

A lightweight structured extraction test was conducted using:

- `requests`
- `BeautifulSoup`
- CSS selectors identified through manual DOM inspection

Results:

| Platform | Candidate Review Blocks Found | Sample Review Text Extracted |
|---|---:|---|
| Google Play Store | 3 | Yes |
| Apple App Store | 8 | Yes |
| Amazon | 0 | No |

Both Google Play Store and Apple App Store successfully exposed identifiable individual review blocks through the lightweight HTML extraction approach.

Google Play Store returned three candidate review blocks, while Apple App Store returned eight. The difference in block count should not be interpreted as evidence that one platform is inherently easier to collect, because each page may expose a different number of reviews in its initial HTML response.

Amazon produced a different result. Review-specific elements were visible during manual inspection of the browser-rendered DOM, but the same review containers were not identified in the HTML returned through the basic Python request.

This suggests that a simple `requests` and `BeautifulSoup` workflow may not consistently reproduce the Amazon review structure visible in a fully rendered browser.

---

## Key Results

| Dimension | Amazon | Google Play Store | Apple App Store |
|---|---|---|---|
| Business Value | Very High | Very High | High |
| Product Coverage | Very High | Medium–High | Medium–High |
| Metadata Richness | High | Very High | High |
| Initial HTTP Accessibility | Successful | Successful | Successful |
| Observed Repeatability | Low–Medium | High in limited testing | High in limited testing |
| Lightweight Review Extraction | Not successful | Successful | Successful |
| Initial Workflow Suitability | Low–Medium | Medium–High | Medium–High |

The detailed reasoning behind these assessments is documented in [`assessment.md`](./assessment.md).

---

## Phase II: Large-Scale Collection and Analysis

Following the Phase I source assessment, Phase II expands the project into large-scale review collection and exploratory analysis using Google Play Store and Apple App Store in parallel.

The Phase II design emphasizes **paired comparisons of the same applications across platforms** rather than relying only on platform-wide averages.

### Sampling Design

The final sampling design includes:

- 28 shared applications
- 6 application categories
- Google Play Store and Apple App Store
- Matched review counts at the application level

The six study categories are:

- Education
- Finance
- Music & Audio
- Productivity & Cloud
- Social & Community
- Travel & Mobility

---

## Phase II Dataset

Large raw datasets were first collected separately from each platform.

The datasets were then processed to:

- Remove duplicate review IDs from the analysis samples
- Match review counts for the same application across platforms
- Preserve the original raw datasets separately
- Maintain application and category identifiers for paired analysis

Final matched analysis datasets:

| Platform | Apps | Reviews |
|---|---:|---:|
| Apple App Store | 28 | 13,599 |
| Google Play Store | 28 | 13,599 |

Matching review counts improves same-app comparability, but does **not** guarantee that the two platforms represent the same historical time window.

---

## Analysis Structure

Phase II analysis is organized into three notebooks.

### `01_data_quality.ipynb`

Examines:

- Missing values
- Duplicate review IDs
- Repeated review text
- Rating distributions
- Review length
- Low-information comments
- Timestamp coverage
- Metadata availability

### `02_paired_app_analysis.ipynb`

Focuses on paired comparisons of the same applications across platforms, including:

- Cross-platform rating gaps
- Timestamp-coverage diagnostics
- Rating distributions for selected paired apps
- Review length and low-signal differences
- Negative-review detail
- Product/business implications

### `03_category_analysis.ipynb`

Examines whether app-level differences extend to broader categories, including:

- Category-level rating differences
- Consistency of rating direction within categories
- Timestamp sensitivity analysis
- Category-level review quality
- Short-review and repeated-text patterns

---

## Preliminary Findings

Current Phase II analysis suggests:

- Cross-platform rating differences are highly application-specific and should not be interpreted using platform-wide averages alone.
- Finance shows one of the more robust category-level Google-higher rating patterns after considering timestamp comparability.
- Social & Community also shows consistently higher Google Play ratings, although substantial timestamp mismatch limits stronger interpretation.
- Apple App Store reviews are longer across all six study categories in the current matched sample.
- Google Play contains a higher proportion of very short and repeated review text across all six categories.
- Lower-rated reviews generally contain more detailed written feedback on both platforms.
- Equal review counts can represent substantially different historical time windows across platforms.
- Platform-specific metadata availability affects which downstream analyses are appropriate.

These findings are descriptive and should not be interpreted as causal platform effects.

### Business Relevance

The analysis suggests that platform choice may affect both observed sentiment and the amount of diagnostic information available in individual reviews.

Apple reviews may provide richer written context per review, while Google Play may require stronger filtering for short or repetitive feedback before text-based sentiment analysis.

At the same time, paired app analysis shows that no single platform consistently produces more positive or negative feedback across all applications. Product teams may therefore benefit from evaluating the same application across both platforms rather than relying on a single platform-wide benchmark.

---

## Repository Structure

```text
review-data-source-assessment/
│
├── README.md
├── assessment.md
├── data_collection_plan.md
├── phase_ii_findings.md
│
├── scripts/
│   ├── practical_test.py
│   ├── review_extraction_test.py
│   ├── collect_google_play.py
│   ├── collect_google_play_multiapp.py
│   ├── collect_google_play_full.py
│   ├── collect_google_play_balanced.py
│   ├── collect_apple_store.py
│   ├── collect_apple_store_multiapp.py
│   ├── collect_apple_store_full.py
│   └── build_balanced_analysis_datasets.py
│
├── notebooks/
│   ├── 01_data_quality.ipynb
│   ├── 02_paired_app_analysis.ipynb
│   └── 03_category_analysis.ipynb
│
└── data/
    ├── raw/
    │   ├── google_play_reviews.csv
    │   ├── google_play_balanced_reviews.csv
    │   ├── apple_store_reviews.csv
    │   └── collection summary / validation outputs
    │
    ├── processed/
    │   ├── google_play_analysis.csv
    │   ├── apple_store_analysis.csv
    │   └── matched_sample_counts.csv
    │
    ├── practical_test_results.csv
    ├── field_availability_results.csv
    └── review_extraction_results.csv
```

### Key Files

#### `assessment.md`

Contains the full Phase I comparison of Amazon, Google Play Store, and Apple App Store, including business assessment, technical assessment, practical testing, and the initial source recommendation.

#### `data_collection_plan.md`

Documents the Phase II sampling strategy, selected applications, expected fields, collection methodology, and data-quality considerations.

#### `phase_ii_findings.md`

Consolidates the main Phase II analytical findings across data quality, paired same-app comparisons, category-level patterns, business implications, limitations, and recommended next steps.

#### `scripts/`

Contains the Phase I feasibility tests, Phase II review-collection scripts, and dataset-preparation workflows.

Key Phase II scripts include:

- `collect_google_play_balanced.py` – collects reviews across the shared Google Play app sample
- `collect_apple_store_full.py` – collects the large-scale Apple App Store sample
- `build_balanced_analysis_datasets.py` – creates the matched datasets used for cross-platform analysis

Earlier single-app and multi-app scripts are retained to document the development and validation of the collection workflow.

#### `notebooks/01_data_quality.ipynb`

Examines missing values, duplicates, repeated text, rating distributions, review length, timestamp coverage, and metadata availability.

#### `notebooks/02_paired_app_analysis.ipynb`

Performs paired same-app comparisons across Google Play Store and Apple App Store.

#### `notebooks/03_category_analysis.ipynb`

Examines category-level consistency, timestamp sensitivity, and review-quality patterns.

#### `data/raw/`

Contains the original large-scale collection outputs.

#### `data/processed/`

Contains the cleaned and matched datasets used for the main Phase II analysis.

---

## Installation

### Requirements

- Python 3
- Pandas
- Requests
- BeautifulSoup4
- Matplotlib
- Jupyter / IPython kernel
- google-play-scraper

Install the required packages:

```bash
python -m pip install pandas requests beautifulsoup4 matplotlib jupyter ipykernel google-play-scraper
```

---

## Running the Project

The repository contains both Phase I feasibility tests and Phase II large-scale collection and analysis workflows.

### Phase I: Practical Tests

Run the basic accessibility and field-availability test:

```bash
python scripts/practical_test.py
```

Run the lightweight review extraction test:

```bash
python scripts/review_extraction_test.py
```

### Phase II: Review Collection

#### Google Play Store

```bash
python scripts/collect_google_play_balanced.py
```

Primary output:

```text
data/raw/google_play_balanced_reviews.csv
```

#### Apple App Store

```bash
python scripts/collect_apple_store_full.py
```

Primary output:

```text
data/raw/apple_store_reviews.csv
```

### Build Matched Analysis Datasets

```bash
python scripts/build_balanced_analysis_datasets.py
```

This creates:

```text
data/processed/apple_store_analysis.csv
data/processed/google_play_analysis.csv
data/processed/matched_sample_counts.csv
```

### Phase II Analysis

The main exploratory analysis is contained in:

```text
notebooks/01_data_quality.ipynb
notebooks/02_paired_app_analysis.ipynb
notebooks/03_category_analysis.ipynb
```

---

## Phase I Recommendation

### Google Play Store

Based on the Phase I business assessment, technical research, and practical testing, **Google Play Store was recommended as the initial data source for a prototype recurring ingestion workflow**.

Both Google Play Store and Apple App Store demonstrated successful lightweight review extraction during the initial feasibility testing.

Google Play Store was preferred because it combined practical extraction feasibility with richer potential analytical metadata and strong downstream analytical potential.

This recommendation served as the starting point for the project rather than a final production-scale source-selection decision.

Phase II therefore expanded the project to include **both Google Play Store and Apple App Store in parallel**, allowing the project to evaluate not only collection feasibility but also differences in review content, ratings, metadata, and analytical value at scale.

Amazon remains an attractive future source because of its broad product coverage and rich customer feedback. However, the current testing showed greater technical uncertainty for a simple recurring public-web workflow.

Apple App Store is a strong secondary candidate. It demonstrated successful lightweight review extraction in the representative-page test and offers useful structured review information, including review titles, ratings, dates, written feedback, and territory-related information.

---

## Limitations

The project has progressed from an initial feasibility assessment into large-scale exploratory analysis, but several limitations remain.

### Collection Limitations

- Public review-access methods may change over time.
- Platform pagination and review availability are not always stable.
- The Apple App Store review feed showed variation in available review depth across collection attempts.
- Google Play and Apple App Store expose different metadata fields, limiting direct comparison of some attributes.
- Public collection methods may not provide the same capabilities as official owner/developer APIs.

### Sampling Limitations

- Review counts are matched by application, but matching record counts does not guarantee matching time periods.
- In many applications, the same number of Apple and Google reviews represents substantially different historical coverage.
- Some applications had fewer available Apple reviews and therefore contributed smaller matched samples.

### Analytical Limitations

- Observed cross-platform differences are descriptive and should not be interpreted as causal platform effects.
- Differences may reflect app-specific events, release timing, user populations, platform behavior, or collection characteristics.
- Repeated review text is not automatically treated as duplicate data because different users may independently submit identical short comments.
- Low-information thresholds such as reviews with 20 characters or fewer are exploratory analytical definitions rather than formal quality standards.

These limitations are considered throughout the paired-app and category-level analyses.

---

## Next Steps

The next stage of the project will build on the Phase II exploratory analysis.

Potential next steps include:

1. Create publication-ready figures for the strongest Phase II findings.
2. Investigate review content more deeply using text-based methods such as sentiment, topic, or issue analysis.
3. Examine whether major rating or sentiment changes align with application-version changes where metadata is available.
4. Develop platform-specific preprocessing rules for short, repetitive, or low-information reviews.
5. Evaluate whether timestamp-aligned sampling improves cross-platform comparability.
6. Compare issue patterns for selected high-value applications across Google Play Store and Apple App Store.
7. Build product-focused reporting outputs from the strongest analytical findings.

A potential future workflow is:

```text
Review Sources
      ↓
Large-Scale Collection
      ↓
Quality Validation
      ↓
Matched Cross-Platform Analysis
      ↓
Text / Sentiment Analysis
      ↓
Product & Business Insights
```

---

## Project Status

**Phase I:** Completed – Data source assessment and feasibility testing

**Phase I Recommendation:** Google Play Store as the initial prototype source

**Phase II:** In Progress – Large-scale Google Play and Apple App Store collection, matched dataset construction, and exploratory cross-platform analysis

**Current Analysis:** Data quality, paired same-app comparison, timestamp sensitivity, and category-level analysis

**Current Dataset:** 28 shared applications across 6 categories, with 13,599 matched reviews per platform

**Next Focus:** Deeper text-based issue analysis, timestamp-aligned comparisons, and product-oriented reporting
