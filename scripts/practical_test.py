import requests
import pandas as pd
from bs4 import BeautifulSoup

urls = {
    "Google Play": "https://play.google.com/store/apps/details?id=com.spotify.music",
    "Apple App Store": "https://apps.apple.com/us/app/spotify-music-and-podcasts/id324684580",
    "Amazon": "PASTE_YOUR_AMAZON_PRODUCT_URL_HERE"
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

        soup = BeautifulSoup(response.text, "html.parser")

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
