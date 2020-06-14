import requests

URL = ""
r = requests.get(url=URL)
js = r.json()
print(js)

