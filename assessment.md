# Review Data Source Assessment

## 1. Executive Summary


This assessment evaluates Amazon, Google Play Store, and Apple App Store as potential sources for building a recurring review-data ingestion workflow to support downstream sentiment analysis.

The three platforms were compared from both business and technical/practical perspectives, including review relevance, review richness, metadata availability, product coverage, public accessibility, repeatability, and suitability for recurring collection.

From a business perspective, Amazon provides the broadest product coverage and highly detailed customer feedback, while Google Play Store and Apple App Store provide more standardized application-focused review data. Google Play Store stands out for its relatively rich technical metadata, which can support version-level, device-level, and broader product-experience analysis.

Lightweight practical testing was conducted using Python `requests`, `BeautifulSoup`, and `pandas`. All three platforms were accessible through basic HTTP requests. Google Play Store and Apple App Store showed relatively consistent page retrieval, while Amazon produced less consistent responses across repeated tests.

In the small review extraction test, both Google Play Store and Apple App Store successfully exposed individual review blocks through the lightweight `requests` and `BeautifulSoup` approach. Three candidate review blocks were identified from Google Play Store and eight from Apple App Store.

Amazon produced a different result. Review-specific elements were visible during manual inspection of the browser-rendered DOM, but the same review containers were not identified in the HTML returned through the basic Python request. This suggests that a simple HTTP-based extraction approach may not be sufficient for reliable Amazon review collection.

Based on the combined business assessment and practical testing, **Google Play Store is recommended as the initial data source for the ingestion workflow**. Both Google Play Store and Apple App Store demonstrated promising lightweight extraction feasibility, but Google Play Store provides a stronger overall combination of rich analytical metadata, standardized app-review data, observed repeatability, and downstream product-analysis potential.

Amazon remains valuable as a potential future source because of its broad product coverage and rich customer feedback, while Apple App Store represents a strong secondary option that also demonstrated successful lightweight review extraction.

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

Amazon review pages contain recognizable review-specific structures in the browser-rendered DOM.

During manual HTML inspection, individual review elements were observed with attributes such as:

- `data-hook="reviewContainer"`
- `data-hook="review"`
- `data-hook="reviewTextContainer"`
- `data-hook="review-by-line"`

These structures suggest that review records are clearly identifiable after the page is fully rendered in a browser.

However, practical testing showed that the same structures were not consistently available in the HTML returned through basic Python `requests`.

Repeated HTTP requests also produced substantially different responses. One request returned a full product page of approximately 1.13 million characters, while a later request returned only approximately 3,781 characters despite both responses having HTTP status code `200`.

In the small extraction test, the manually identified selector `div[data-hook='reviewContainer']` returned zero review blocks from the HTML retrieved through `requests`, even though the same review containers were visible in the browser-rendered DOM.

This distinction suggests that simple HTTP retrieval may not consistently reproduce the final review structure visible to a browser. A more advanced rendering or data-access approach may therefore be required for reliable recurring Amazon review collection.

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

The browser-rendered page clearly exposes structured review elements, indicating that the underlying review data is potentially extractable. However, the lightweight testing showed that these elements were not consistently present in the HTML returned through basic Python HTTP requests.

Combined with the substantial variation observed across repeated responses, this creates additional uncertainty for a simple and maintainable recurring workflow based only on `requests` and `BeautifulSoup`.

A more advanced approach, such as browser rendering or another approved data-access method, may be required before Amazon could be used reliably as a recurring source.

Therefore, Amazon may be better suited as a future or supplementary source rather than the initial source used to prototype the ingestion workflow.

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

Initial practical testing was encouraging. The representative Google Play page was retrieved relatively consistently, and three candidate individual review blocks were successfully identified using a lightweight `requests` and `BeautifulSoup` approach.

Apple App Store also demonstrated successful lightweight review extraction, so extraction feasibility alone does not clearly distinguish the two app platforms. Google Play remains the stronger initial candidate primarily because of its richer technical metadata and broader downstream product-analysis potential.

Additional testing across multiple applications and larger review volumes would still be required before treating the approach as production-ready.


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

During manual DOM inspection, individual review containers were identified using review-specific attributes. The selector `div[aria-labelledby^='review-']` was then tested against the HTML returned through Python `requests`.

The lightweight extraction test successfully identified eight candidate review blocks. The extracted content included review titles, dates, reviewer information, ratings, and written user feedback.

This suggests that, for the representative page tested, Apple App Store reviews were compatible with a lightweight `requests` and `BeautifulSoup` extraction approach.

However, the current test used only one representative application. Additional testing across multiple applications and repeated runs would still be required before assuming that the same structure is consistently reusable.

**Assessment: High for owned apps; Medium to High for public-page collection in limited testing**

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

For applications owned or managed by an organization, Apple App Store review data appears highly suitable for a recurring workflow because the official App Store Connect API provides structured review access.

For general public applications, the initial practical results were also encouraging. The representative page was retrieved relatively consistently, and eight candidate individual elements were successfully identified using a lightweight `requests` and `BeautifulSoup` approach.

This indicates that Apple App Store is a viable candidate for a lightweight public-web ingestion prototype.

However, the current evidence is limited to one application and a small number of tests. Broader validation across multiple applications, repeated requests, and larger review volumes would still be required before considering the workflow production-ready.

**Assessment: Medium to High**

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
| Repeatability | High for owned apps; Medium to High in limited public-page testing |
| Recurring Workflow Suitability | Medium to High |

### Preliminary Conclusion

Apple App Store is a strong candidate for sentiment-analysis data.

Its major strengths include structured written reviews, numerical ratings, review dates, and territory information. Territory-level data may be particularly useful for comparing customer feedback across different geographic markets.

Compared with Google Play, Apple provides somewhat less technical metadata because Google Play may include additional information related to app versions, operating systems, devices, language, and helpful-vote information.

Like Google Play, Apple's official developer API is primarily designed for applications managed by the developer rather than unrestricted public third-party review collection.

Initial practical testing was encouraging. The Apple App Store representative page was retrieved relatively consistently, and eight candidate individual elements were successfully identified using the lightweight `requests` and `BeautifulSoup` approach.

Therefore, Apple App Store should be considered a strong technical alternative to Google Play Store. Google Play remains the preferred initial source primarily because of its richer analytical metadata and broader downstream product-analysis potential rather than because of a unique extraction advantage.

Additional testing across multiple applications would still be required before treating either public-page approach as production-ready.

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

A small structured extraction test was conducted to evaluate whether individual review blocks could be identified directly from the HTML returned by each platform.

Before running the test, the browser-rendered DOM for each platform was manually inspected to identify review-specific HTML structures. These observed CSS selectors were then tested against HTML retrieved using Python `requests` and parsed with `BeautifulSoup`.

The objective was not to build a production scraper, but to determine whether individual review records could be identified using a lightweight extraction approach.

| Platform | Status Code | Selector Used | Candidate Review Blocks Found | Sample Review Text Extracted |
|---|---:|---|---:|---|
| Google Play Store | 200 | `div[data-g-id='reviews'] > div:has(> header[data-review-id])` | 3 | Yes |
| Apple App Store | 200 | `div[aria-labelledby^='review-']` | 8 | Yes |
| Amazon | 200 | `div[data-hook='reviewContainer']` | 0 | No |

Google Play Store successfully exposed three candidate individual review blocks. The extracted content included information that appeared to represent actual user reviews.

Apple App Store also produced a successful result. Eight candidate review blocks were identified, and sample review content could be extracted from the returned HTML.

Amazon produced a different result. During manual inspection of the browser-rendered DOM, review-specific structures such as `data-hook="reviewContainer"` were clearly visible. However, the same selector returned zero review blocks when applied to the HTML retrieved through the basic Python `requests` workflow.

This finding highlights an important distinction between the browser-rendered DOM and the HTML returned through a basic HTTP request. Review content that is visible after the page is rendered in a browser may not necessarily be present in the same form in the initial HTML response.

Therefore, the Amazon result should not be interpreted as evidence that the platform contains no accessible reviews. Instead, it suggests that a simple `requests` and `BeautifulSoup` approach may not be sufficient to retrieve the same review structure consistently.

These results are limited to one representative page per platform and a small-scale feasibility test. They should therefore be interpreted as initial comparative evidence rather than proof of production-level extraction reliability.

### 7.5 Practical Testing Summary

The practical tests revealed meaningful differences among the three sources.

All three platforms were initially accessible through basic HTTP requests and returned status code `200`. However, successful HTTP retrieval alone did not guarantee that individual review records could be identified or extracted consistently.

Google Play Store performed well in the lightweight testing. Its page responses were relatively consistent, several review-related fields were identifiable, and individual review content was successfully extracted using `requests` and `BeautifulSoup`. 

Apple App Store also demonstrated strong initial feasibility. Its public page responses were relatively consistent, and review-related content was also successfully identified using the same lightweight extraction approach.

The different numbers of matched elements should not be interpreted as evidence that one platform is inherently easier to collect than the other. The more important finding is that review content was identifiable for both platforms.
The different numbers of review blocks found on Google Play Store and Apple App Store should not be interpreted as evidence that one platform is inherently easier to collect than the other. The pages may expose different numbers of reviews in their initial HTML responses. The more important finding is that individual review structures were successfully identified for both platforms.

Amazon demonstrated greater technical uncertainty. Although review containers were clearly visible during manual inspection of the browser-rendered DOM, the same structures were not identified in the HTML returned through the basic Python request. Amazon also produced substantially different response sizes across repeated HTTP tests.

Overall, the practical testing suggests the following:

1. **Google Play Store** – strong lightweight extraction feasibility and relatively consistent retrieval.
2. **Apple App Store** – similarly strong initial extraction feasibility and relatively consistent retrieval.
3. **Amazon** – high business value, but greater uncertainty for a simple `requests` and `BeautifulSoup` workflow.

When practical feasibility is considered together with business and analytical value, Google Play Store remains the preferred initial source primarily because of its richer technical metadata and broader downstream product-analysis potential.

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
| Lightweight Review Extraction | Not successful | Successful | Successful |
| Recurring Workflow Suitability | Low to Medium | **Medium to High** | Medium to High |

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

Google Play Store provides a strong combination of business value, rich metadata, and practical accessibility.

Its main strengths include:

- Rich written user feedback
- Ratings and review dates
- App-version and technical metadata
- Strong potential for sentiment and product analysis
- Relatively consistent page responses during testing
- Successful identification of individual review blocks using a lightweight extraction approach

The main limitation is that Google's official developer review API is primarily intended for applications managed by the developer. Public or competitor-app review collection therefore requires a separate public-web collection approach.

The practical testing showed that Google Play and Apple App Store were both compatible with the lightweight extraction approach. Therefore, Google Play's main comparative advantage is not unique extraction feasibility, but its richer technical metadata and broader potential for version-level, device-level, and product-experience analysis.

#### Apple App Store

Apple App Store also provides high-quality user feedback and useful structured information such as ratings, review titles, review text, dates, and territory.

Its main strengths include:

- Strong sentiment-analysis potential
- Useful geographic information through territory data
- Relatively consistent page accessibility
- Structured official review access for owned applications
- Successful lightweight extraction of individual review blocks

In the practical test, review-related elements were successfully identified using the selector `div[aria-labelledby^='review-']`, and sample review content could be extracted from the returned HTML.

This places Apple App Store close to Google Play Store from an initial public-page extraction-feasibility perspective.

The main trade-off relative to Google Play is metadata depth. Google Play may provide additional technical information related to app versions, operating systems, devices, language, and helpful-vote information, which can support a broader range of downstream product analysis.

### 8.3 Comparative Conclusion

The comparison shows that no single source is strongest across every criterion.

Amazon provides the broadest product coverage and very rich customer feedback, giving it strong business and analytical value. However, it showed the greatest technical uncertainty during practical testing. Review structures were visible in the browser-rendered DOM, but the same review containers were not identified in the HTML returned through the lightweight Python request. Amazon also produced less consistent responses across repeated tests.

Google Play Store and Apple App Store both demonstrated successful lightweight review extraction and relatively consistent public-page retrieval.

Apple App Store performed strongly from an extraction-feasibility perspective, with review-related content successfully identified and extracted from the representative page.

Google Play Store also demonstrated successful extraction and provides richer potential technical metadata, including app-version, operating-system, device, language, and helpful-vote information.

Therefore, the practical testing alone does not clearly separate Google Play Store and Apple App Store. When technical feasibility is combined with metadata richness and downstream analytical potential, **Google Play Store provides the strongest overall balance for the initial ingestion workflow**.

Apple App Store should be considered a strong secondary candidate, while Amazon may be more appropriate for future expansion if a more reliable and approved collection method is identified.

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

These fields could support not only basic sentiment classification but also deeper product-level analysis, such as identifying version-related sentiment changes, recurring technical issues, and feature feedback.

### 9.2 Strong Balance Between Richness and Structure

Amazon provides broader product diversity, but Google Play review data is more standardized because reviews are associated with applications that follow a relatively consistent product structure.

This consistency may simplify:

- Data normalization
- Schema design
- Cross-app comparison
- Recurring ingestion
- Downstream analytical workflows

Apple App Store also provides relatively standardized application-review data, but Google Play offers richer potential technical metadata that may support a wider range of product and user-experience analysis.

### 9.3 Strong Practical Feasibility with Richer Metadata

Both Google Play Store and Apple App Store demonstrated successful lightweight review extraction during the practical testing.

Three candidate review blocks were identified from the representative Google Play page, while eight were identified from the Apple App Store page.

The difference in the number of blocks should not be interpreted as evidence that one platform is inherently easier to collect than the other, because the initial HTML responses may expose different numbers of reviews.

The key finding is that both platforms demonstrated compatibility with a lightweight `requests` and `BeautifulSoup` approach.

Google Play is preferred because it combines this successful extraction feasibility with richer potential metadata, including app-version, operating-system, device, language, and helpful-vote information.

By comparison, Amazon showed greater technical uncertainty. Review structures were visible in the browser-rendered DOM, but the same review containers were not identified in the HTML returned through the basic Python request. Amazon also produced less consistent responses across repeated tests.

### 9.4 Suitable Starting Point for an Iterative Workflow

The objective of the initial implementation should not be to support every possible review source immediately.

Starting with Google Play would allow the team to develop and validate the core workflow:

`Collect -> Clean -> Structure -> Store -> Analyze`

Once this workflow is stable, Apple App Store could be evaluated as the next source because it also demonstrated promising lightweight extraction feasibility.

Amazon could be reconsidered later if a more reliable and approved collection method becomes available.

### Recommendation Summary

Google Play Store is recommended because it provides the strongest overall balance across:

- Business relevance
- Review richness
- Metadata availability
- Analytical potential
- Observed repeatability
- Initial extraction feasibility

Apple App Store is a strong secondary candidate and demonstrated successful lightweight review extraction in the representative-page test.

Amazon should remain a potential future source because of its broad product coverage and rich customer feedback, but the current testing suggests greater technical uncertainty for a simple recurring public-web collection workflow.

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
