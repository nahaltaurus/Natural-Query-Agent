import requests
from bs4 import BeautifulSoup
import pandas as pd
import re
def scrape_lecture_notes(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find('div', class_='content')
    if content:
        return content.get_text()
    else:
        return f"Unable to find content for {url}"

def scrape_model_architectures(url):
    tables = pd.read_html(url)
    return tables[0]  # Assuming the first table is the one we want

urls = {
    'harms-1': 'https://stanford-cs324.github.io/winter2022/lectures/harms-1/',
    'introduction': 'https://stanford-cs324.github.io/winter2022/lectures/introduction/',
    'training': 'https://stanford-cs324.github.io/winter2022/lectures/training/',
    'legality': 'https://stanford-cs324.github.io/winter2022/lectures/legality/'
}


lecture_contents = {}
for key, url in urls.items():
    lecture_name = key  # Use the dictionary key as the lecture name
    lecture_contents[lecture_name] = scrape_lecture_notes(url)


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


lecture_contents = {}
for key, url in urls.items():
     content = fetch_and_extract_content(url)
     lecture_name = key  # Use the dictionary key as the lecture name
     lecture_contents[lecture_name] = content


architectures_url = "https://github.com/Hannibal046/Awesome-LLM#milestone-papers"
model_architectures = scrape_model_architectures(architectures_url)

all_data = {**lecture_contents, "model_architectures": model_architectures.to_json()}

print(all_data)
