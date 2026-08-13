import requests

APP_ID = "324684580"
APP_NAME = "Spotify"
COUNTRY = "us"

MAX_PAGES_TO_TEST = 20

all_ids = set()
total_entries = 0

print(f"Testing Apple pagination depth for {APP_NAME}...\n")

for page in range(1, MAX_PAGES_TO_TEST + 1):

    url = (
        f"https://itunes.apple.com/{COUNTRY}/rss/"
        f"customerreviews/page={page}/"
        f"id={APP_ID}/sortby=mostrecent/json"
    )

    try:
        response = requests.get(
            url,
            timeout=15
        )

    except Exception as e:
        print(f"Page {page}: request error - {e}")
        break

    print(
        f"Page {page}: "
        f"status={response.status_code}",
        end=""
    )

    if response.status_code != 200:
        print(" | stopped")
        break

    try:
        data = response.json()

    except Exception as e:
        print(f" | JSON error: {e}")
        break

    entries = (
        data.get("feed", {})
        .get("entry", [])
    )

    if not entries:
        print(" | entries=0 | stopped")
        break

    page_ids = []

    for review in entries:

        review_id = (
            review.get("id", {})
            .get("label")
        )

        page_ids.append(review_id)

    duplicate_with_previous = sum(
        review_id in all_ids
        for review_id in page_ids
    )

    unique_on_page = len(
        set(page_ids)
    )

    print(
        f" | entries={len(entries)}"
        f" | unique={unique_on_page}"
        f" | repeated_from_previous={duplicate_with_previous}"
    )

    all_ids.update(page_ids)
    total_entries += len(entries)


print("\n" + "=" * 50)
print("PAGINATION TEST SUMMARY")
print("=" * 50)

print("Total entries returned:", total_entries)
print("Unique review IDs:", len(all_ids))
print(
    "Repeated IDs:",
    total_entries - len(all_ids)
)
