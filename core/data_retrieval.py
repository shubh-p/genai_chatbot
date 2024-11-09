import json
import requests
from bs4 import BeautifulSoup

def fetch_gitlab_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Extract relevant content based on specific tags or classes
        content = soup.find_all('p')  # Adjust selectors as needed
        return [p.get_text() for p in content]
    else:
        print("Failed to retrieve data")
        return []

handbook_data = fetch_gitlab_data('https://about.gitlab.com/company/')
direction_data =fetch_gitlab_data('https://about.gitlab.com/direction/')
# Save the processed data to a JSON file
with open('data/gitlab_handbook.json', 'w') as f:
    json.dump(handbook_data, f)
with open('data/gitlab_direction.json', 'w') as f:
    json.dump(direction_data, f)

print("Data saved to data/gitlab_handbook.json")
print("Data saved to data/gitlab_direction.json")

