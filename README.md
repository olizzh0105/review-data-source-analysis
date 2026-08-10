# Review Data Source Assessment

This project evaluates **Amazon, Google Play Store, and Apple App Store** as potential sources for building a recurring review-data ingestion workflow for downstream sentiment analysis.

The assessment considers both:

- Business value
- Technical feasibility
- Public accessibility
- Review richness
- Metadata availability
- Repeatability
- Suitability for recurring collection

A small amount of practical testing was also conducted using Python to compare how easily review-related data could be accessed and extracted from each platform.

## Research Question

Which of Amazon, Google Play Store, and Apple App Store is the most suitable source for building a recurring review-data ingestion workflow for downstream sentiment analysis?

## Key Finding

Based on the combined business assessment and practical testing, **Google Play Store is recommended as the initial data source**.

Google Play provided the strongest overall balance of:

- Review relevance
- Metadata richness
- Analytical potential
- Stable page accessibility
- Repeatability
- Initial review extraction feasibility

Amazon provides very rich customer feedback and broad product coverage, but showed lower repeatability during lightweight HTTP testing.

Apple App Store also provides high-quality review data and relatively stable accessibility, but individual review blocks were not successfully extracted using the lightweight public-page approach tested in this project.

## Practical Testing

The technical assessment included three lightweight tests:

1. **Basic Programmatic Accessibility Test**
   - Used Python `requests` to retrieve representative public pages.
   - All three platforms initially returned HTTP status code `200`.

2. **Review Field Availability Test**
   - Checked for review-related information such as:
     - review
     - rating
     - date
     - version
     - author
     - helpful

3. **Small Review Extraction Test**
   - Used `BeautifulSoup` and candidate CSS selectors to identify individual review blocks.
   - Google Play Store was the only platform where candidate individual review text was successfully extracted using the tested approach.

These tests are intended as an initial feasibility assessment rather than a production-scale scraping implementation.

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
