# Review Data Source Assessment

## 1. Executive Summary

This assessment evaluates Amazon, Google Play Store, and Apple App Store as potential sources for building a recurring review-data ingestion workflow to support downstream sentiment analysis.

The three platforms were compared from both business and technical/practical perspectives, including review relevance, review richness, metadata availability, product coverage, public accessibility, repeatability, and suitability for recurring collection.

From a business perspective, Amazon provides the broadest product coverage and highly detailed customer feedback, while Google Play Store and Apple App Store provide more standardized application-focused review data. Google Play Store stands out for its relatively rich technical metadata, including information that can support version-level, device-level, and product-experience analysis.

Lightweight practical testing was also conducted using Python `requests`, `BeautifulSoup`, and `pandas`. All three platforms were initially accessible through basic HTTP requests. However, repeated testing showed that Amazon responses were less consistent, while Google Play Store and Apple App Store demonstrated more stable page retrieval. In a small review extraction test, Google Play Store was the only platform from which candidate individual review text was successfully identified using the lightweight extraction approach.

Based on the combined business assessment and practical testing, **Google Play Store is recommended as the initial data source for the ingestion workflow**. It provides the strongest overall balance of analytical value, structured metadata, observed repeatability, and initial extraction feasibility.

Amazon remains valuable as a potential future source because of its broad product coverage and rich customer feedback, while Apple App Store represents a strong secondary option that may require a different extraction or data-access approach.

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
| Data Structure | Whether review-related information can be identified and extracted from the returned page content |
| Repeatability | Whether collection can be repeated consistently |
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

### 4.2 Technical / Practical Perspective

#### Public Accessibility

Amazon customer reviews are visible through public product pages, making the data observable without requiring access to a private internal database.

However, public visibility does not necessarily mean that the data is easy or appropriate to collect automatically at scale. The feasibility of automated collection must therefore be evaluated separately from simple browser accessibility.

**Assessment: High**

#### Official API Availability

Amazon provides programmatic access to product catalog information through its Creators API.

However, the currently documented Creators API resources focus on information such as:

- Product information
- Images
- Offers
- Product variations
- Browse nodes
- Search refinements

Customer review text is not listed as a supported resource in the current Creators API documentation.

This means that the official product API does not appear to provide a straightforward method for retrieving large volumes of customer review text for this use case.

**Assessment: Low**

#### Data Structure and Repeatability

Amazon product and review pages generally follow recognizable layouts, which suggests that review information may be technically identifiable from public-facing pages.

However, a recurring data ingestion workflow would require more than identifying individual fields. The system would need to consistently handle:

- Multiple products
- Multiple review pages
- Pagination
- Changes in page structure
- Missing or inconsistent review fields
- Request failures or access restrictions

Therefore, the repeatability of large-scale collection cannot be assumed based only on manual browser access.

Practical testing showed inconsistent responses across repeated requests. While one request returned a full product page, a later request returned a substantially smaller response despite the same HTTP status code `200`.

This suggests that simple public-web collection may have lower repeatability for Amazon.

**Assessment: Low to Medium**

#### Restrictions and Operational Risk

Amazon appears less suitable for unrestricted automated collection than the two app-store alternatives.

Because customer review text is not directly exposed as a standard resource through the current Creators API, a recurring workflow may have to depend more heavily on public-web collection.

This introduces additional concerns related to:

- Platform terms and acceptable-use requirements
- Automated-access restrictions
- Changes in webpage structure
- Potential anti-automation mechanisms
- Long-term maintenance requirements

Any production-scale implementation would therefore require a more detailed review of Amazon's applicable terms and approved data-access methods before automated collection is implemented.

**Assessment: Low to Medium**

#### Suitability for a Recurring Workflow

Amazon has very high business value but lower technical practicality for the proposed recurring ingestion system.

The data itself could support sophisticated sentiment and product analysis, but reliable long-term collection may require significantly more engineering effort and platform-specific maintenance than other sources.

Therefore, Amazon may be better suited as a future or supplementary data source rather than the initial source used to prototype the ingestion workflow.

**Assessment: Low to Medium**

### 4.3 Overall Assessment

| Criterion | Amazon Assessment |
|---|---|
| Review Relevance | High |
| Review Richness | Very High |
| Product Coverage | Very High |
| Metadata Richness | High |
| Analytical Potential | Very High |
| Public Accessibility | High |
| Official Review API Accessibility | Low |
| Repeatability | Low to Medium |
| Recurring Workflow Suitability | Low to Medium |

### Preliminary Conclusion

Amazon is arguably the strongest of the three sources from a business-data perspective because of its broad product coverage and rich customer feedback. The review text could support detailed sentiment analysis, pain-point identification, and product-level comparisons.

However, Amazon appears less attractive from a technical and operational perspective. The current official Creators API focuses primarily on product catalog information rather than customer review text, meaning that recurring review collection may require a more complex public-web approach.

For this reason, Amazon should remain an important candidate, but it may not be the best source for the initial implementation of a simple and maintainable recurring ingestion workflow.

## 5. Google Play Store

### 5.1 Business Perspective

#### Review Relevance

Google Play reviews provide direct feedback from users about their experiences with Android applications. Users can provide both star ratings and written reviews, making the data useful for understanding customer satisfaction, usability issues, feature preferences, and technical problems.

Because reviews are associated with specific applications, the feedback is particularly relevant for analyzing digital product performance and user experience.

**Assessment: High**

#### Review Richness

Google Play reviews can provide both qualitative and quantitative information.

Useful review information may include:

- Written review text
- Star rating
- Review timestamp
- Reviewer language
- App version
- Android OS version
- Device information
- Helpful-vote counts
- Developer response

This combination of written feedback and technical metadata can make Google Play especially useful for identifying whether negative user experiences are associated with a specific app version, operating system, or device.

For example, users may discuss:

- App crashes
- Login problems
- Performance
- User interface
- Subscription pricing
- Advertisements
- New features
- Battery consumption

This creates strong opportunities for both sentiment analysis and product-level analysis.

**Assessment: Very High**

#### Product Coverage

Google Play contains a large range of Android applications and games across categories such as:

- Entertainment
- Productivity
- Finance
- Healthcare
- Education
- Transportation
- Social media
- Retail
- Gaming

However, its product coverage is narrower than Amazon because Google Play primarily represents software applications rather than physical consumer products.

For a project focused on digital products and user experience, this narrower scope may also provide more consistent and comparable feedback.

**Assessment: Medium to High**

#### Metadata Richness

Google Play provides relatively rich review metadata.

Potentially useful fields include:

- Review ID
- Reviewer name
- Review text
- Star rating
- Review date
- Reviewer language
- App version
- Android version
- Device information
- Helpful-vote counts

The availability of app-version and device-related information can support deeper analysis beyond basic positive and negative sentiment classification.

For example, the data could help identify whether negative reviews increased after a specific software update.

**Assessment: Very High**

#### Analytical Potential

Google Play review data could support several types of downstream analysis:

1. **Sentiment Analysis**
   - Classify reviews as positive, neutral, or negative.

2. **Feature and Pain Point Analysis**
   - Identify frequently praised or criticized app features.

3. **Version-Level Analysis**
   - Determine whether user sentiment changes following an app update.

4. **Technical Issue Analysis**
   - Identify recurring problems such as crashes, bugs, login failures, or performance issues.

5. **Device and OS Analysis**
   - Examine whether certain problems are concentrated among specific devices or operating-system versions.

6. **Rating vs. Review Analysis**
   - Compare numerical star ratings with the sentiment expressed in written reviews.

7. **Trend Analysis**
   - Track changes in user satisfaction and recurring issues over time.

These use cases make Google Play particularly valuable for product analytics and digital customer-experience analysis.

**Assessment: Very High**

#### Business Limitations

Google Play review data also introduces several potential limitations.

First, the platform primarily represents Android applications, making it less suitable for analyzing customer sentiment toward physical products.

Second, users who choose to leave reviews may not represent the full user population, which can introduce selection bias.

Third, review quality varies significantly. Some users provide detailed feedback, while others leave very short comments.

Users may also update their ratings and reviews over time, meaning that individual review records can change.

Overall, these limitations should be considered when interpreting results, but they do not substantially reduce the value of Google Play reviews for application-focused sentiment analysis.

---

### 5.2 Technical / Practical Perspective

#### Public Accessibility

Google Play reviews are publicly visible through application pages.

However, there is an important difference between data being visible to users and data being freely available through an official API.

Google's official developer tools are primarily designed for developers accessing reviews associated with applications they manage.

Initial practical testing also showed that a representative public Google Play page could be retrieved successfully through a basic HTTP request without login. The page returned a complete response with review-related content, and candidate individual review text was later identified using the lightweight extraction approach.

Therefore, public browser accessibility appears high, while programmatic collection of arbitrary third-party applications still requires broader testing across multiple apps before its general reliability can be established.

**Assessment: High for public accessibility**

#### Official API Availability

Google provides an official review API through the Google Play Developer API.

The API can provide structured review data and supports programmatic retrieval of reviews for applications managed by the developer.

However, it should not be treated as a completely public API for collecting reviews from any application on Google Play.

Important limitations include:

- Authentication is required
- Access is primarily designed for apps managed by the developer
- The API focuses on written reviews
- API quotas and retrieval limitations may apply

Therefore, the official API is highly useful for first-party applications but less useful for unrestricted public or competitor-app review collection.

**Assessment: High for owned apps; Low to Medium for general public apps**

#### Data Structure and Repeatability

For authorized applications, Google Play provides a highly structured and repeatable review format.

The data can potentially support a recurring workflow such as:

`Retrieve reviews -> clean data -> store data -> analyze sentiment`

Structured fields such as rating, review text, date, app version, and device information make the data relatively straightforward to normalize and store in a relational database.

Initial practical testing showed relatively consistent public-page retrieval for Google Play Store, and candidate individual review text was successfully extracted from the representative page using a lightweight `requests` and `BeautifulSoup` approach.

However, the current test used only one representative application. Additional testing across multiple apps would be needed to determine whether the extraction structure is consistently reusable.

**Assessment: High for owned apps; Medium to High for public-page collection**

#### Restrictions and Operational Risk

The primary limitation is authorization.

Using Google's official developer tools requires appropriate developer access and permissions.

Additional considerations may include:

- API quotas
- Authentication requirements
- Restrictions on accessing third-party applications
- Changes in public webpage structure
- Maintenance requirements for public-web collection

Compared with Amazon, Google Play appears to provide a more standardized environment for review data.

**Assessment: Medium**

#### Suitability for a Recurring Workflow

Google Play appears highly suitable for a recurring review workflow when the application is managed by the organization collecting the data.

Its combination of structured review text, ratings, timestamps, app versions, and technical metadata creates strong opportunities for automated analysis.

For public third-party applications, the initial practical testing was encouraging: the tested page was retrieved consistently and candidate individual review text could be extracted using a lightweight public-web approach.

However, broader testing across multiple applications, repeated runs, and larger review volumes would still be required before considering the workflow production-ready.

**Assessment: Medium to High**

---

### 5.3 Overall Assessment

| Criterion | Google Play Assessment |
|---|---|
| Review Relevance | High |
| Review Richness | Very High |
| Product Coverage | Medium to High |
| Metadata Richness | Very High |
| Analytical Potential | Very High |
| Public Accessibility | High |
| Official Review API Accessibility | High for owned apps; Low to Medium for public apps |
| Repeatability | High for owned apps; Medium to High in limited public-page testing |
| Recurring Workflow Suitability | Medium to High |

### Preliminary Conclusion

Google Play Store provides a strong balance between business value and technical feasibility.

Its major advantage is the richness of its metadata. In addition to written reviews and ratings, review data may include app-version, operating-system, device, language, and helpful-vote information.

This creates opportunities not only for sentiment analysis but also for identifying technical issues, monitoring product updates, and understanding changes in customer experience.

The main limitation is that Google's official developer tools are primarily designed for applications managed by the developer rather than unrestricted public review collection.

Therefore, Google Play appears to be a strong candidate for the initial ingestion workflow. The practical testing conducted in this assessment supports this conclusion, as Google Play showed relatively consistent page retrieval and was the only tested platform from which candidate individual review text was successfully extracted using the lightweight approach.

Additional testing across multiple applications would still be needed before treating the approach as production-ready.


## 6. Apple App Store

### 6.1 Business Perspective

#### Review Relevance

Apple App Store reviews contain direct feedback from users regarding their experiences with applications.

Users can provide numerical ratings and written reviews, creating useful signals about:

- Customer satisfaction
- Usability
- Product features
- Technical issues
- Pricing
- Customer expectations

Because reviews are tied to individual applications, they are highly relevant for analyzing digital product performance and customer experience.

**Assessment: High**

#### Review Richness

Apple App Store reviews provide both numerical ratings and written feedback.

Useful review information may include:

- Star rating
- Review title
- Review body
- Reviewer nickname
- Review date
- Territory

Written reviews may include feedback about:

- Application usability
- Performance
- Bugs and crashes
- Subscription pricing
- Feature requests
- Interface design
- Recent updates
- Overall customer experience

The combination of review titles and written review bodies creates useful text for sentiment and topic analysis.

However, Apple generally provides less device-specific metadata than Google Play.

**Assessment: High**

#### Product Coverage

The Apple App Store represents applications across many categories, including:

- Entertainment
- Finance
- Healthcare
- Productivity
- Education
- Social networking
- Gaming
- Transportation
- Shopping

Like Google Play, the App Store primarily represents software products rather than physical consumer goods.

Therefore, its product coverage is narrower than Amazon but highly relevant for digital-product analysis.

**Assessment: Medium to High**

#### Metadata Richness

Apple App Store reviews contain several useful structured fields, including:

- Rating
- Review title
- Review body
- Reviewer nickname
- Review date
- Territory

The territory field is particularly useful because it may support geographic or market-level comparison.

Review data may also be connected to specific application versions, creating opportunities for analyzing changes in customer feedback over time.

Compared with Google Play, however, Apple provides less detailed device and operating-system metadata through its basic review structure.

**Assessment: High**

#### Analytical Potential

Apple App Store review data could support several types of analysis:

1. **Sentiment Analysis**
   - Identify positive, neutral, and negative user feedback.

2. **Feature Analysis**
   - Identify frequently requested or criticized features.

3. **Pain Point Analysis**
   - Detect recurring usability or technical problems.

4. **Rating vs. Review Analysis**
   - Compare written sentiment with numerical star ratings.

5. **Territory Analysis**
   - Compare feedback patterns across geographic markets.

6. **Version-Related Analysis**
   - Examine whether customer feedback changes following application updates.

7. **Trend Analysis**
   - Track changes in customer sentiment over time.

These analyses could help product teams understand customer expectations and prioritize product improvements.

**Assessment: Very High**

#### Business Limitations

Apple App Store data is primarily limited to Apple's software ecosystem.

This reduces its usefulness for businesses seeking feedback across physical-product categories.

As with the other platforms, review data may also contain selection bias because users who voluntarily leave reviews may not represent the entire customer population.

Review length and detail can vary significantly, and users may also modify their reviews over time.

In addition, geographic differences may influence ratings and review behavior across different App Store territories.

These factors should be considered when interpreting sentiment-analysis results.

---

### 6.2 Technical / Practical Perspective

#### Public Accessibility

Customer ratings and written reviews are publicly visible through App Store product pages.

However, public visibility does not necessarily mean that the reviews can be freely collected through an official public API.

Apple's official App Store Connect tools are primarily designed for developers managing their own applications.

**Assessment: Medium to High**

#### Official API Availability

Apple provides an official App Store Connect API for retrieving customer reviews associated with applications managed through App Store Connect.

The API provides structured review information and can support automated processing.

However, API access requires authentication and appropriate App Store Connect permissions.

Therefore, the API is useful for first-party application data but should not be considered an unrestricted public API for competitor reviews.

**Assessment: High for owned apps; Low to Medium for general public apps**

#### Data Structure and Repeatability

For authorized applications, Apple provides structured review data that can be integrated relatively easily into an automated workflow.

Fields such as:

- Rating
- Title
- Review body
- Date
- Territory

can be converted into structured tables and stored for downstream analysis.

A potential recurring workflow could follow the structure:

`Retrieve reviews -> normalize fields -> store data -> analyze sentiment`

Initial practical testing showed relatively consistent public-page retrieval for the Apple App Store representative page.

However, the lightweight HTML extraction test did not successfully identify individual review blocks using the tested selectors. This suggests that basic public-page access is relatively stable, but structured review extraction may require a different extraction method or data-access approach.

**Assessment: High for owned apps; Medium for public-page collection in limited testing**

#### Restrictions and Operational Risk

The primary technical limitation is authentication and ownership-based access.

Important considerations include:

- API authentication requirements
- App Store Connect permissions
- Access primarily to applications managed by the organization
- Territory-specific data
- Different collection requirements for third-party applications
- Potential maintenance requirements for public-web collection

Compared with Amazon, Apple provides a clearer structured review API for developers.

However, its usefulness for an open-web ingestion workflow depends on whether the project requires first-party or third-party review data.

**Assessment: Medium**

#### Suitability for a Recurring Workflow

For applications owned or managed by an organization, Apple App Store review data appears highly suitable for a recurring workflow.

Its structured review attributes can support automated collection, cleaning, storage, and sentiment analysis.

For general public applications, initial testing showed relatively consistent page accessibility, but individual review blocks were not successfully extracted using the lightweight HTML approach tested in this assessment.

This suggests that Apple App Store remains a feasible candidate, but additional technical work may be required before it can support a simple recurring public-web collection workflow.

**Assessment: Medium**

---

### 6.3 Overall Assessment

| Criterion | Apple App Store Assessment |
|---|---|
| Review Relevance | High |
| Review Richness | High |
| Product Coverage | Medium to High |
| Metadata Richness | High |
| Analytical Potential | Very High |
| Public Accessibility | Medium to High |
| Official Review API Accessibility | High for owned apps; Low to Medium for public apps |
| Repeatability | High for owned apps; Medium in limited public-page testing |
| Recurring Workflow Suitability | Medium |

### Preliminary Conclusion

Apple App Store is another strong candidate for sentiment-analysis data.

Its major strengths include structured written reviews, numerical ratings, review dates, and territory information. Territory-level data may be particularly useful for comparing customer feedback across different geographic markets.

Compared with Google Play, Apple appears slightly less rich in technical metadata because Google Play may provide additional information related to app versions, operating systems, and devices.

Like Google Play, Apple's main technical limitation is that its official developer API is primarily designed for applications managed by the developer rather than unrestricted public third-party review collection.

Initial practical testing showed that Apple App Store public pages could be retrieved relatively consistently, but the lightweight HTML extraction approach did not successfully identify individual review blocks.

Therefore, Apple App Store remains a strong secondary candidate, but it appears to require a different extraction or data-access approach than Google Play for public third-party review collection.

## 7. Practical Testing

### Test Scope

The practical assessment used one representative public page from each platform:

- **Amazon:** Echo Dot product page
- **Google Play Store:** Spotify application page
- **Apple App Store:** Spotify application page

Testing was conducted in GitHub Codespaces using Python with `requests`, `BeautifulSoup`, and `pandas`.

The tests were designed as lightweight feasibility checks rather than production-scale scraping experiments. Results should therefore be interpreted as initial comparative evidence and may not generalize to all products or applications on each platform.

### 7.1 Basic Programmatic Accessibility Test

A lightweight Python test was conducted to examine whether public pages from each platform could be retrieved through a basic HTTP request.

The test used Python `requests` to retrieve one representative public page from each platform. The response status code, HTML page size, page title, and presence of review-related content were recorded.

| Platform | Status Code | Page Size | Review-Related Content Detected |
|---|---:|---:|---|
| Amazon | 200 | 1,129,258 | Yes |
| Google Play Store | 200 | 1,336,455 | Yes |
| Apple App Store | 200 | 760,017 | Yes |

All three platforms successfully returned HTTP status code `200`, indicating that the tested public pages could be retrieved through basic programmatic requests.

Google Play Store returned the largest HTML response at approximately 1.34 million characters, followed by Amazon at approximately 1.13 million and Apple App Store at approximately 0.76 million.

Review-related content was detected in the returned HTML for all three platforms.

Based on this initial test, no major difference in basic HTTP accessibility was observed among Amazon, Google Play Store, and Apple App Store.

However, successful page retrieval does not necessarily mean that individual review records can be extracted easily or consistently. Additional testing is required to evaluate review-field availability and structured review extraction.

### 7.2 Review-Related Keyword Presence Test

A second lightweight test was conducted to examine whether several review-related keywords were present in the text returned from each platform.

The test searched for the following terms:

- `review`
- `rating`
- `date`
- `version`
- `author`
- `helpful`

The purpose of this test was not to confirm successful structured extraction, but to determine whether potentially useful review-related information could be identified in the returned page content.

| Keyword | Google Play Store | Apple App Store | Amazon |
|---|---|---|---|
| Review | Yes | Yes | Yes |
| Rating | Yes | Yes | No |
| Date | Yes | Yes | Yes |
| Version | Yes | Yes | Yes |
| Author | No | No | No |
| Helpful | Yes | No | No |

Google Play Store showed the broadest range of review-related keywords in the returned page text, including review, rating, date, version, and helpful-related information.

Apple App Store also showed review, rating, date, and version-related keywords, although author and helpful-related terms were not detected.

Amazon showed fewer identifiable review-related keywords during this test. Review, date, and version-related terms were detected, while rating, author, and helpful-related terms were not detected.

These results should be interpreted cautiously. Keyword presence does not confirm that the corresponding data field can be reliably extracted for individual review records. A structured extraction test is still required.

### 7.3 Repeatability Observation

An important difference was observed across repeated HTTP tests.

Google Play Store and Apple App Store returned relatively consistent page responses across multiple runs. In contrast, Amazon produced substantially different responses between two tests.

In an earlier test, the Amazon page returned:

- HTTP status code: `200`
- Page size: approximately `1.13 million` characters
- Review-related content detected: Yes

In a later test, the same Amazon request returned:

- HTTP status code: `200`
- Page size: approximately `3,781` characters
- Page title: `Amazon.com`
- Review-related content detected: No

This suggests that HTTP status code alone is not sufficient to determine whether the complete Amazon product page has been retrieved.

The variation observed across repeated requests may indicate lower repeatability for a simple public-web collection workflow. Additional testing would be required before relying on Amazon as a stable recurring data source.

### 7.4 Small Review Extraction Test

A small structured extraction test was conducted to evaluate whether individual review-like text blocks could be identified directly from the HTML returned by each platform.

The test used Python `requests` and `BeautifulSoup` and attempted several candidate CSS selectors for each platform. The objective was not to build a production scraper, but to determine whether individual review records appeared readily identifiable using a lightweight extraction approach.

| Platform | Status Code | Selector Used | Candidate Review Blocks Found | Sample Review Text Extracted |
|---|---:|---|---:|---|
| Google Play Store | 200 | `div.h3YV2d` | 3 | Yes |
| Apple App Store | 200 | None | 0 | No |
| Amazon | 200 | None | 0 | No |

Google Play Store was the only platform in this test for which candidate individual review text could be identified and extracted using the lightweight `requests` and `BeautifulSoup` approach.

Three candidate review blocks were detected from the Google Play page, and the extracted content included text that appeared to represent actual user feedback.

For Apple App Store, the public page was successfully retrieved with HTTP status code `200`, but none of the tested CSS selectors identified individual review blocks. This suggests that review content may require a different extraction method or data-access approach.

Amazon also returned HTTP status code `200`, but no individual review blocks were identified during this test. Combined with the inconsistent page responses observed in the repeatability test, this suggests that a simple HTML-based recurring collection workflow may be less reliable for Amazon.

These results are limited to one representative page per platform and a small set of candidate selectors. Therefore, they should be interpreted as an initial feasibility comparison rather than evidence of production-level extraction reliability.

### 7.5 Practical Testing Summary

The practical tests revealed meaningful differences among the three sources.

All three platforms were initially accessible through basic HTTP requests, with each returning status code `200`. Therefore, basic page accessibility alone did not provide a strong basis for distinguishing between the sources.

However, differences became clearer as the testing progressed.

Google Play Store showed the strongest performance in the lightweight tests. Its page responses were relatively consistent, several review-related fields were identifiable, and candidate individual review text could be extracted using a simple `requests` and `BeautifulSoup` workflow.

Apple App Store also demonstrated relatively consistent basic accessibility and contained several useful review-related fields. However, the lightweight extraction test did not successfully identify individual review blocks using the tested selectors.

Amazon demonstrated the greatest uncertainty. Although an initial request successfully returned a full product page, a later request returned a substantially smaller response despite the same HTTP status code. Individual review blocks were also not identified during the structured extraction test.

Overall, the practical testing suggests the following initial technical ranking for a lightweight public-web collection workflow:

1. **Google Play Store** – strongest initial feasibility
2. **Apple App Store** – accessible and structured, but individual review extraction requires further investigation
3. **Amazon** – high business value but lower observed repeatability and greater extraction uncertainty

These findings will be considered together with the business-value assessment in the final comparative evaluation and recommendation.

## 8. Comparative Assessment

The three review-data sources were compared using both the business and technical/practical criteria defined earlier in this assessment, together with the results of the lightweight practical tests.

### 8.1 Overall Comparison

| Criterion | Amazon | Google Play Store | Apple App Store |
|---|---|---|---|
| Review Relevance | High | High | High |
| Review Richness | Very High | Very High | High |
| Product Coverage | Very High | Medium to High | Medium to High |
| Metadata Richness | High | Very High | High |
| Analytical Potential | Very High | Very High | Very High |
| Public Browser Accessibility | High | High | High |
| Official Review API for Owned Apps | Low | High | High |
| Basic HTTP Accessibility | Successful | Successful | Successful |
| Repeatability in Practical Testing | Low to Medium | High in limited testing | High in limited testing |
| Review-Related Keyword Presence | Medium | High | High |
| Lightweight Review Extraction | Not successful | Successful | Not successful |
| Recurring Workflow Suitability | Low to Medium | **Medium to High** | Medium |

### 8.2 Key Trade-Offs

#### Amazon

Amazon provides the broadest product coverage and some of the richest customer review content among the three sources.

Its main strengths include:

- Large variety of product categories
- Detailed customer feedback
- Strong potential for aspect-based sentiment analysis
- Opportunities for product and competitor comparison

However, the practical testing raised concerns about repeatability. Although the Amazon page initially returned a complete response, a later request returned a much smaller page despite still returning HTTP status code `200`.

The lightweight extraction test also did not successfully identify individual review blocks.

Therefore, Amazon offers very strong business value but introduces greater technical uncertainty for a simple recurring public-web ingestion workflow.

#### Google Play Store

Google Play Store provides a strong combination of business value, structured metadata, and practical accessibility.

Its main strengths include:

- Rich written user feedback
- Ratings and review dates
- App-version and technical metadata
- Strong potential for sentiment and product analysis
- Relatively consistent page responses during testing
- Successful identification of candidate individual review text using a lightweight extraction approach

The main limitation is that Google's official developer review API is primarily intended for applications managed by the developer. Public or competitor-app review collection therefore requires a separate public-web collection approach.

Despite this limitation, Google Play performed best in the practical testing conducted for this assessment.

#### Apple App Store

Apple App Store also provides high-quality user feedback and useful structured information such as ratings, review text, dates, and territory.

Its main strengths include:

- Strong sentiment-analysis potential
- Useful geographic information through territory data
- Relatively consistent page accessibility
- Structured official review access for owned applications

However, the lightweight public-page extraction test did not successfully identify individual review blocks using the tested selectors.

This does not mean that App Store reviews cannot be collected, but it suggests that additional extraction methods or data-access approaches may be required.

### 8.3 Comparative Conclusion

The comparison shows that no single source is strongest across every criterion.

Amazon provides the broadest business coverage and very rich customer feedback, but it showed the greatest technical uncertainty during practical testing.

Apple App Store provides high-quality and structured application feedback, but individual review extraction was not successful using the lightweight public-web approach tested in this assessment.

Google Play Store provides the strongest overall balance. It offers rich analytical metadata, strong sentiment-analysis potential, relatively consistent accessibility, and was the only platform from which candidate individual review text was successfully extracted using the lightweight testing approach.

Based on the combination of business value and observed technical feasibility, Google Play Store appears to be the most suitable source for the initial recurring review-data ingestion workflow.


## 9. Recommendation

### Recommended Source: Google Play Store

Based on the business assessment, technical research, and practical testing, **Google Play Store is recommended as the initial data source for the review-data ingestion workflow**.

The recommendation is based on four main factors.

### 9.1 Strong Analytical Value

Google Play reviews provide both qualitative and quantitative information that can support downstream analysis.

Potential analytical fields include:

- Review text
- Star rating
- Review date
- App version
- Reviewer language
- Device or operating-system information
- Helpful-vote information

These fields could support not only basic sentiment classification but also product-level analysis such as version-related sentiment changes, recurring technical issues, and feature feedback.

### 9.2 Strong Balance Between Richness and Structure

Amazon provides richer product diversity, but Google Play review data is more standardized because reviews are associated with applications that follow a relatively consistent product structure.

This consistency may simplify:

- Data normalization
- Schema design
- Cross-app comparison
- Recurring ingestion
- Downstream analytical workflows

### 9.3 Strongest Practical Testing Result

Google Play performed best in the lightweight practical testing.

The public page:

- Successfully returned HTTP status code `200`
- Produced relatively consistent responses across repeated tests
- Contained multiple review-related fields
- Allowed candidate individual review text to be identified using `requests` and `BeautifulSoup`

By comparison, Amazon showed inconsistent responses across repeated requests, while Apple App Store did not expose individual review blocks through the selectors tested.

This provides initial evidence that Google Play may require less technical complexity for an early prototype.

### 9.4 Suitable Starting Point for an Iterative Workflow

The objective of the first implementation should not be to immediately support every possible review source.

Starting with Google Play would allow the team to develop and validate the core workflow:

`Collect -> Clean -> Structure -> Store -> Analyze`

Once this workflow is stable, additional sources such as Apple App Store or Amazon could be evaluated for integration.

### Recommendation Summary

Google Play Store is recommended because it provides the strongest balance across:

- Business relevance
- Review richness
- Metadata availability
- Analytical potential
- Observed repeatability
- Initial extraction feasibility

Amazon should remain a potential future source because of its high business value, while Apple App Store represents a strong secondary source for future expansion.

The recommendation is based on a limited feasibility test using representative public pages and should therefore be treated as the preferred source for an initial prototype rather than a final production-scale architecture decision.


## 10. Next Steps

If Google Play Store is selected as the initial source, the next phase should focus on validating whether the initial findings can be translated into a small, repeatable ingestion workflow.

### 10.1 Validate Extraction Across Multiple Apps

The current practical test used one representative application.

The next step should test the extraction approach on several additional Google Play applications to determine whether the observed review structure is consistent across different apps.

This would help evaluate whether the extraction logic is reusable rather than specific to one application.

### 10.2 Define the Initial Review Data Schema

A standardized review structure should be defined before larger-scale collection begins.

Potential fields include:

- `source`
- `app_id`
- `app_name`
- `review_text`
- `rating`
- `review_date`
- `app_version`
- `reviewer_language`
- `helpful_count`
- `collection_timestamp`

The schema can be refined depending on which fields are consistently available during extraction.

### 10.3 Build a Small Repeatable Collection Prototype

A lightweight ingestion script could then be developed to:

1. Retrieve review data
2. Extract selected fields
3. Handle missing values
4. Normalize the output
5. Save the results in a structured format

The first prototype could use CSV files for validation before introducing a relational database.

### 10.4 Evaluate Data Quality

The collected sample should be checked for:

- Missing fields
- Duplicate reviews
- Inconsistent ratings
- Invalid dates
- Very short or empty review text
- Changes in page structure

These checks would help determine whether the source is reliable enough for downstream sentiment analysis.

### 10.5 Prepare for Structured Storage

Once the extraction process is sufficiently stable, the cleaned review data could be stored in a relational database such as SQLite for local prototyping.

A simple initial structure could separate:

- Applications
- Reviews
- Collection metadata

This would support SQL-based analysis and future integration with downstream sentiment-analysis workflows.

### 10.6 Reassess Additional Sources

After the Google Play workflow is validated, Apple App Store could be evaluated as the next potential source.

Amazon may also be reconsidered if a more reliable and approved method of accessing customer review data becomes available.

This staged approach would allow the project to prioritize a technically manageable source first while preserving the option to expand the ingestion system later.
