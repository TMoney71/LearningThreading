import requests

response = requests.get('http://127.0.0.1:8790')
data = response.json()
#print(data)
films = data['films']
#print(films)
response = requests.get(films + '6')
print(response.json())