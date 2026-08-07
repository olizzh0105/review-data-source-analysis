# Review Data Source Assessment

## 1. Executive Summary

## 2. Research Question

Which of Amazon, Google Play Store, and Apple App Store is the most suitable source for building a recurring review-data ingestion workflow for downstream sentiment analysis?

## 3. Evaluation Criteria

The three data sources are evaluated from two main perspectives: business value and technical feasibility.

### 3.1 Business Perspective

| Criteria | Description |
|---|---|
| Review Relevance | How well the reviews reflect actual user experiences |
| Review Richness | How detailed and informative the review content is |
| Product Coverage | The range of products or businesses represented |
| Metadata Richness | Availability of ratings, dates, versions, and other metadata |
| Analytical Potential | Types of downstream analysis that can be performed |
| Limitations | Potential biases or weaknesses in the data |

### 3.2 Technical / Practical Perspective

| Criteria | Description |
|---|---|
| Public Accessibility | Whether data can be accessed without login |
| Data Structure | How structured and consistent the available data is |
| Repeatability | Whether collection can be repeated consistently |
| Pagination | Whether large volumes of reviews can be collected |
| Restrictions | API, scraping, or platform restrictions |
| Recurring Workflow Suitability | Suitability for ongoing automated collection |

## 4. Amazon

Amazon is a potentially valuable review-data source because it contains large volumes of product-level customer feedback across a wide range of product categories. From a business perspective, the platform offers rich opportunities for sentiment and customer-experience analysis. However, its technical feasibility for a recurring ingestion workflow is less straightforward because programmatic access to customer review data is limited.

### 4.1 Business Perspective

#### Review Relevance

Amazon customer reviews are directly tied to users' experiences and opinions about specific products. Reviews can therefore provide useful signals about customer satisfaction, product quality, feature preferences, and common pain points.

Amazon also distinguishes some reviews with a "Verified Purchase" badge when the product was purchased through Amazon. However, Amazon allows eligible users to review products even if they did not purchase the product through Amazon, meaning that not all reviews represent verified Amazon transactions.

**Assessment: High**

#### Review Richness

Amazon reviews can provide both quantitative and qualitative information. Depending on the review, useful information may include:

- Star rating
- Written review text
- Review title
- Review date
- Verified Purchase status
- Helpful-vote information

The written review text can be particularly valuable because customers often discuss multiple dimensions of a product rather than simply indicating whether they like or dislike it.

For example, a review of wireless headphones may discuss:

- Sound quality
- Battery life
- Comfort
- Connectivity
- Durability
- Price and value

This makes Amazon data especially useful for more detailed, aspect-based sentiment analysis.

One limitation is that some customers may provide only a star rating without detailed written feedback, reducing the amount of textual information available for sentiment modeling.

**Assessment: Very High**

#### Product Coverage

Amazon has broad product coverage across categories such as electronics, household products, clothing, beauty products, books, appliances, and many other consumer goods.

Compared with Google Play Store and Apple App Store, which primarily represent software applications, Amazon can provide customer feedback across a much wider variety of physical and digital product categories.

This broad coverage could make Amazon particularly useful if the future analytics platform is intended to support multiple industries rather than only mobile applications.

**Assessment: Very High**

#### Metadata Richness

Amazon reviews contain several useful pieces of metadata that could support downstream analysis, including ratings and indicators such as Verified Purchase status.

Product-level information could also potentially be connected to review data, allowing analysis by:

- Product
- Brand
- Product category
- Rating level
- Review period

However, the accessibility and consistency of these fields would need to be confirmed through practical testing before designing a recurring workflow.

**Assessment: High**

#### Analytical Potential

Amazon review data could support several types of downstream business analysis.

Potential use cases include:

1. **Sentiment Analysis**
   - Classify reviews as positive, neutral, or negative.

2. **Aspect-Based Sentiment Analysis**
   - Identify which product attributes customers like or dislike.

3. **Pain Point Identification**
   - Detect frequently mentioned problems such as poor battery life, product defects, or difficult setup.

4. **Rating vs. Text Analysis**
   - Compare numerical star ratings with the sentiment expressed in written reviews.

5. **Product and Competitor Comparison**
   - Compare customer feedback across similar products or brands.

6. **Trend Analysis**
   - Track how customer sentiment changes over time.

These analyses could ultimately help businesses understand customer needs, prioritize product improvements, and identify competitive strengths and weaknesses.

**Assessment: Very High**

#### Business Limitations

Despite its analytical value, Amazon review data also introduces several potential limitations.

First, review data may suffer from selection bias because customers who choose to leave reviews may not represent the entire customer population.

Second, not all reviews are verified purchases. Amazon states that eligible customers may review products even when the product was purchased elsewhere, although Amazon identifies qualifying Amazon purchases with a Verified Purchase badge.

Third, the amount of written information varies significantly across reviews. Some reviews are detailed, while others contain very little text or only a star rating.

Finally, review moderation and removal may cause the available dataset to change over time.

Overall, these limitations do not eliminate the business value of Amazon reviews, but they should be considered when interpreting sentiment-analysis results.

## 5. Google Play Store

## 6. Apple App Store

## 7. Comparative Assessment

## 8. Recommendation

## 9. Next Steps
