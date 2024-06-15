import json

# Function to load JSON data from a file
def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

# Function to structure data by keywords
def structure_data_by_keywords(data):
    structured_data = {}
    for item in data:
        keywords = item.get('Keywords')  # Assuming 'Keywords' is the correct key based on your example
        if keywords:
            structured_data[keywords] = item
    return structured_data

# Paths to your files
data2_filepath = r'C:\Users\91918\Music\ml prj\data2.json'
output_filepath = r'C:\Users\91918\Music\structured_data123.json'

# Load data from JSON file
data2 = load_json(data2_filepath)

# Structure the data by keywords
structured_data = structure_data_by_keywords(data2)

# Save structured data to a new JSON file
with open(output_filepath, 'w', encoding='utf-8') as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=4)

print(f"Structured data saved to {output_filepath}")
