import requests

url = "http://127.0.0.1:5001/auth"

payload = "{\n\t\"username\": \"Sulman\",\n\t\"password\": \"abc123\"\n}"
headers = {
  'Content-Type': 'application/json'
}

response = requests.request("POST", url, headers=headers, data = payload)

print(response.text.encode('utf8'))