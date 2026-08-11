import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = {
    "Google Play": "https://play.google.com/store/apps/details?id=com.spotify.music",
    "Apple App Store": "https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580",
    "Amazon": "https://www.amazon.com/Amazon-vibrant-helpful-routines-Charcoal/dp/B09B8V1LZ3"
}

headers = {
    "User-Agent": "Mozilla/5.0"
}

# Candidate CSS selectors.
# We are testing whether any of these structures expose review blocks.
selectors = {
    "Google Play": [
        "div[data-g-id='reviews'] > div:has(> header[data-review-id])"
    ],

    "Apple App Store": [
        "div[aria-labelledby^='review-']"
    ],

    "Amazon": [
        "div[data-hook='reviewTextContainer']"
    ]
}

results = []

for platform, url in urls.items():

    print(f"\nTesting {platform}...")

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=15
        )

        soup = BeautifulSoup(
            response.content,
            "html.parser"
        )

        selector_used = None
        review_elements = []

        # Try each possible selector
        for selector in selectors[platform]:

            elements = soup.select(selector)

            if len(elements) > 0:
                selector_used = selector
                review_elements = elements
                break

        # Extract text from the first few candidate review blocks
        review_texts = []

        for element in review_elements[:5]:

            text = element.get_text(
                " ",
                strip=True
            )

            if text:
                review_texts.append(text)

        print("Status code:", response.status_code)
        print("Selector used:", selector_used)
        print("Review blocks found:", len(review_elements))

        if review_texts:
            print("\nSample extracted text:")

            for i, text in enumerate(review_texts[:3], start=1):
                print(f"{i}. {text[:300]}")

        else:
            print("No individual review text extracted.")

        results.append({
            "platform": platform,
            "status_code": response.status_code,
            "selector_used": selector_used,
            "review_blocks_found": len(review_elements),
            "sample_review_1": review_texts[0] if len(review_texts) > 0 else "",
            "sample_review_2": review_texts[1] if len(review_texts) > 1 else "",
            "sample_review_3": review_texts[2] if len(review_texts) > 2 else ""
        })

    except Exception as e:

        print("Error:", e)

        results.append({
            "platform": platform,
            "status_code": "Error",
            "selector_used": "",
            "review_blocks_found": 0,
            "sample_review_1": "",
            "sample_review_2": "",
            "sample_review_3": ""
        })


df = pd.DataFrame(results)

df.to_csv(
    "data/review_extraction_results.csv",
    index=False
)

print("\n\nFinal Extraction Results")
print(
    df[
        [
            "platform",
            "status_code",
            "selector_used",
            "review_blocks_found"
        ]
    ].to_string(index=False)
)
