# Review Data Source Assessment

This project evaluates **Amazon, Google Play Store, and Apple App Store** as potential sources for building a recurring review-data ingestion workflow for downstream sentiment analysis.

The assessment combines **business evaluation, technical research, and lightweight practical testing** to identify the source that provides the strongest balance between analytical value and implementation feasibility.

> [!NOTE]
> **Recommended initial source: Google Play Store**
>
> Based on the current assessment and practical testing, both Google Play Store and Apple App Store demonstrated successful lightweight review extraction. Google Play Store is recommended because it provides the strongest overall balance of review richness, technical metadata, repeatability, extraction feasibility, and downstream analytical potential.

---

## Outline

- [Overview](#overview)
- [Research Question](#research-question)
- [Evaluation Framework](#evaluation-framework)
- [Data Sources](#data-sources)
- [Practical Testing](#practical-testing)
- [Key Results](#key-results)
- [Repository Structure](#repository-structure)
- [Installation](#installation)
- [Running the Tests](#running-the-tests)
- [Recommendation](#recommendation)
- [Limitations](#limitations)
- [Next Steps](#next-steps)

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
| Pagination | Ability to expand collection beyond an initial page |
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
| Observed Repeatability | Low–Medium | High | High |
| Lightweight Review Extraction | Not successful | Successful | Successful |
| Initial Workflow Suitability | Low–Medium | Medium–High | Medium–High |

The detailed reasoning behind these assessments is documented in [`assessment.md`](./assessment.md).

---

## Repository Structure

```text
review-data-source-assessment/
│
├── README.md
├── assessment.md
│
├── scripts/
│   ├── practical_test.py
│   └── review_extraction_test.py
│
└── data/
    ├── practical_test_results.csv
    ├── field_availability_results.csv
    └── review_extraction_results.csv
```

### Files

#### `assessment.md`

Contains the full comparison of Amazon, Google Play Store, and Apple App Store, including:

- Business assessment
- Technical assessment
- Practical testing
- Comparative evaluation
- Final recommendation
- Next steps

#### `scripts/practical_test.py`

Performs lightweight testing for:

- HTTP accessibility
- Page size
- Page title
- Review-related content
- Review-field availability

#### `scripts/review_extraction_test.py`

Attempts to identify candidate individual review blocks using public webpage HTML and `BeautifulSoup`.

#### `data/`

Contains CSV outputs generated from the practical testing scripts.

---

## Installation

### Requirements

- Python 3
- Requests
- BeautifulSoup4
- Pandas

Install the required packages:

```bash
python -m pip install requests beautifulsoup4 pandas
```

---

## Running the Tests

### Basic Accessibility and Field Test

```bash
python scripts/practical_test.py
```

This generates:

```text
data/practical_test_results.csv
data/field_availability_results.csv
```

### Small Review Extraction Test

```bash
python scripts/review_extraction_test.py
```

This generates:

```text
data/review_extraction_results.csv
```

---

## Recommendation

### Google Play Store

Based on the combined business assessment, technical research, and practical testing, **Google Play Store is recommended as the initial data source for a prototype recurring ingestion workflow**.

Both Google Play Store and Apple App Store demonstrated successful lightweight review extraction using `requests` and `BeautifulSoup`.

Google Play Store is preferred because it combines this practical feasibility with richer potential analytical metadata, including app-version, operating-system, device, language, and helpful-vote information.

This creates broader opportunities for downstream analysis such as:

- Sentiment analysis
- Version-level sentiment tracking
- Technical issue identification
- Feature and pain-point analysis
- Device or operating-system comparisons
- Trend analysis

Amazon remains an attractive future source because of its broad product coverage and rich customer feedback. However, the current testing showed greater technical uncertainty for a simple recurring public-web workflow.

Apple App Store is a strong secondary candidate. It demonstrated successful lightweight review extraction in the representative-page test and offers useful structured review information, including review titles, ratings, dates, written feedback, and territory-related information.

The recommendation should therefore be interpreted as a practical starting point for the initial prototype rather than a final production-scale source-selection decision.

---

## Limitations

This project is an **initial feasibility assessment**, not a production-scale ingestion implementation.

Current limitations include:

- One representative page was tested per platform
- Only a small number of HTTP requests were performed
- Candidate CSS selectors may change over time
- Successful extraction was not tested across multiple products or applications
- Official developer APIs may provide different capabilities for applications owned by the organization
- Platform terms, rate limits, and approved access methods should be reviewed before any production-scale automated collection

The practical results should therefore be interpreted as **comparative evidence for selecting an initial prototype source**, rather than proof of long-term production reliability.

---

## Next Steps

If Google Play Store is selected as the initial source, the next phase should:

1. Test the extraction approach across multiple applications.
2. Define a standardized review-data schema.
3. Extract a larger sample of review records.
4. Normalize ratings, dates, text, and metadata.
5. Add basic data-quality validation.
6. Store cleaned review records in a structured format.
7. Prototype relational storage using SQLite.
8. Prepare the dataset for downstream sentiment analysis.

A possible future workflow is:

```text
Review Source
     ↓
Data Collection
     ↓
Cleaning & Validation
     ↓
Structured Storage
     ↓
Sentiment Analysis
     ↓
Business Insights
```

---

## Project Status

**Current Phase:** Data source assessment and feasibility testing

**Recommended Source:** Google Play Store

**Next Phase:** Small repeatable ingestion prototype
