import json
import requests
from bs4 import BeautifulSoup

def fetch_gitlab_data(url):
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        sections = []
        
        # Identify headers to create meaningful chunks
        for header in soup.find_all(['h2', 'h3']):  # Adjust based on HTML structure
            content = []
            for sibling in header.find_next_siblings():
                if sibling.name in ['h2', 'h3']:
                    break  # New section starts
                if sibling.name == 'p':
                    content.append(sibling.get_text())
            if content:
                sections.append({"header": header.get_text(), "content": " ".join(content)})
        return sections
    else:
        print("Failed to retrieve data")
        return []

handbook_data = fetch_gitlab_data('https://about.gitlab.com/company/')
direction_data =fetch_gitlab_data('https://about.gitlab.com/direction/')
# Save the processed data to a JSON file
with open('data/gitlab_handbook.json', 'w') as f:
    json.dump(handbook_data, f, indent=2)
with open('data/gitlab_direction.json', 'w') as f:
    json.dump(direction_data, f, indent=2)

print("Data saved to data/gitlab_handbook.json")
print("Data saved to data/gitlab_direction.json")

