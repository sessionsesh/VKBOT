import requests
# api: 819012f85e3fd2b9d0da0e7916b318dc
response = requests.get('http://api.openweathermap.org/data/2.5/weather?q=moscow&appid=819012f85e3fd2b9d0da0e7916b318dc&units=metric')
info = response.json()

print(info['main']['temp'])