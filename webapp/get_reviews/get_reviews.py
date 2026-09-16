from serpapi import GoogleSearch

params = {
  "engine": "google_maps_reviews",
  "data_id": "0x2e7881a84f19c03b:0x87990377e6ee814b",  # Data ID dari lokasi kamu
  "api_key": "d324c81daaa4b9761f9549eefefab840a56493830aefbef25793fd8525b3c846"
}

search = GoogleSearch(params)
results = search.get_dict()

for review in results["reviews"]:
    print(f"{review['user']['name']} ({review['rating']}★): {review['snippet']}")

