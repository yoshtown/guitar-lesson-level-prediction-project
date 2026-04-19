import requests

response = requests.post(
    "http://127.0.0.1:5001/predict",
    json={
        "title": "Easy beginner guitar lesson for kids",
        "description": "Learn your first chords"
    }
)

print(response.status_code)
print(response.text)
print(response.json())