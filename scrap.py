import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
import json


urls = {
    'harms-1': 'https://stanford-cs324.github.io/winter2022/lectures/harms-1/',
    'introduction': 'https://stanford-cs324.github.io/winter2022/lectures/introduction/',
    'training': 'https://stanford-cs324.github.io/winter2022/lectures/training/',
    'legality': 'https://stanford-cs324.github.io/winter2022/lectures/legality/'
}


def fetch_and_extract_content(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        div_content = soup.find('div', class_='main-content')
        if div_content:
            # Extract text and clean it
            text = div_content.get_text(separator='\n')  # Preserve newline as separator
            # Remove unwanted symbols but keep periods
            cleaned_text = re.sub(r'[^\w\s\'.]+', '', text)
            cleaned_text = re.sub(r'\s+', ' ', cleaned_text)
            return cleaned_text
        else:
            return f"Div with class 'main-content' not found on {url}"
    except requests.exceptions.RequestException as e:
        return f"Error fetching {url}: {str(e)}"


results = []


for key, url in urls.items():
    content = fetch_and_extract_content(url)
    results.append({'Title': key, 'Content': content})
    print(f"Fetched content for '{key}' from {url}")

df = pd.DataFrame(results)

csv_file = 'lecture_content9.csv'
df.to_csv(csv_file, index=False, encoding='utf-8')
print(f"Content saved to '{csv_file}'")


lectures_json = df.to_dict(orient='records')
json_file = 'lectures0.json'
with open(json_file, 'w') as f:
    json.dump(lectures_json, f, indent=4)
print(f"Content saved to '{json_file}'")
