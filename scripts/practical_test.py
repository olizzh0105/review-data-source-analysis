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

results = []

for platform, url in urls.items():

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        soup = BeautifulSoup(response.content, "html.parser")

        title = soup.title.get_text(strip=True) if soup.title else "Not found"

        results.append({
            "platform": platform,
            "status_code": response.status_code,
            "page_size": len(response.text),
            "page_title": title,
            "contains_review_word": "review" in response.text.lower()
        })

        print(f"{platform}: Success")

    except Exception as e:

        results.append({
            "platform": platform,
            "status_code": "Error",
            "page_size": 0,
            "page_title": "",
            "contains_review_word": False
        })

        print(f"{platform}: {e}")


df = pd.DataFrame(results)

print("\nPractical Test Results")
print(df)

df.to_csv(
    "data/practical_test_results.csv",
    index=False
)

# --------------------------------------------------
# Review-related field availability test
# --------------------------------------------------

print("\nReview-related Field Test")

keywords = [
    "review",
    "rating",
    "date",
    "version",
    "author",
    "helpful"
]

field_results = []

for platform, url in urls.items():

    try:
        response = requests.get(
            url,
            headers=headers,
            timeout=10
        )

        # Use response content directly to reduce encoding issues
        soup = BeautifulSoup(response.content, "html.parser")
        html = soup.get_text(" ", strip=True).lower()

        result = {
            "platform": platform
        }

        for keyword in keywords:
            result[keyword] = keyword in html
            result[f"{keyword}_count"] = html.count(keyword)

        field_results.append(result)

    except Exception as e:
        print(f"{platform}: {e}")


field_df = pd.DataFrame(field_results)

print("\nField Availability Results")
print(field_df.to_string(index=False))

field_df.to_csv(
    "data/field_availability_results.csv",
    index=False
)