import requests

utterance = 'What temperature is it?'
URL = f'https://api.wit.ai/message?v=20200613&q={utterance}'
server_Token = '7IK75DZYLY6JPGO45KNY5HLCMAEGIKB4'
auth_Header = {'Authorization': f'Bearer {server_Token}'}

response = requests.get(url=URL, headers=auth_Header)
js = response.json()

print(js)
