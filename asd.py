import json


def load_json(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        return json.load(f)

def structure_data_by_keywords(data):
    structured_data = {}
    for item in data:
        keywords = item.get('Keywords')  
        if keywords:
            structured_data[keywords] = item
    return structured_data


data2_filepath = r'C:\Users\91918\Music\ml prj\data2.json'
output_filepath = r'C:\Users\91918\Music\structured_data123.json'


data2 = load_json(data2_filepath)

#
structured_data = structure_data_by_keywords(data2)

# 
with open(output_filepath, 'w', encoding='utf-8') as f:
    json.dump(structured_data, f, ensure_ascii=False, indent=4)

print(f"Structured data saved to {output_filepath}")
