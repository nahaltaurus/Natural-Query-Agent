import json

lectures_json = [{'title': title, 'content': content} for title, content in lectures.items()]
with open('lectures.json', 'w') as f:
    json.dump(lectures_json, f)
