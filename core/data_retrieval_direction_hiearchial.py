from bs4 import BeautifulSoup
import json
import requests

# Load HTML content from URL
url = 'https://about.gitlab.com/direction/'
html_content = requests.get(url).text
soup = BeautifulSoup(html_content, 'html.parser')

# Define header and content tags
header_tags = ["h1", "h2", "h3", "h4", "h5", "h6"]
content_tags = ["p", "li"]

# Function to determine header level
def get_header_level(tag_name):
    return int(tag_name[1])

# Recursive data structure to store headers, subheaders, and content
data = []
current_section = None
section_stack = []

for tag in soup.find_all(header_tags + content_tags):
    if tag.name in header_tags:
        level = get_header_level(tag.name)
        
        # Create a new section for the header
        new_section = {
            "header": tag.get_text(strip=True),
            "content": "",
            "subsections": []
        }
        
        # Determine where to place this header in the hierarchy
        while section_stack and get_header_level(section_stack[-1]["header_tag"]) >= level:
            section_stack.pop()
        
        if section_stack:
            # Add as a subsection to the previous header
            section_stack[-1]["subsections"].append(new_section)
        else:
            # This is a top-level header
            data.append(new_section)
        
        # Push the new section onto the stack
        new_section["header_tag"] = tag.name  # Temporary field to track header level
        section_stack.append(new_section)
        
    elif tag.name in content_tags and section_stack:
        # Add content to the current section
        if tag.name == "li":
            # Handle bullet points separately
            if "bullet_points" not in section_stack[-1]:
                section_stack[-1]["bullet_points"] = []
            section_stack[-1]["bullet_points"].append(tag.get_text(strip=True))
        else:
            # Append regular content
            section_stack[-1]["content"] += " " + tag.get_text(strip=True)

# Remove the temporary "header_tag" used for level tracking
def clean_section(section):
    section.pop("header_tag", None)
    for subsection in section["subsections"]:
        clean_section(subsection)

for section in data:
    clean_section(section)

# Convert to JSON and save
json_data = json.dumps(data, ensure_ascii=False, indent=2)
with open("data/webpage_data_hiearchial.json", "w", encoding="utf-8") as f:
    f.write(json_data)

print(json_data)  # Print JSON data to verify
