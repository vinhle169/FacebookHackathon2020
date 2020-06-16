import requests

class wit:

    def __init__(self, utter):
        self.utterance = utter
        URL = f'https://api.wit.ai/message?v=20200615&q={self.utterance}'
        server_Token = 'XHAXSXINWBD5KFLNDL5AQWXO4O7672EC'
        auth_Header = {'Authorization': f'Bearer {server_Token}'}
        response = requests.get(url=URL, headers=auth_Header).json()
        self.intent = response['intents'][0]['name']
        self.entities = {val[0]['name']: (val[0]['value'], val[0]['confidence']) for val in response['entities'].values()}

        if 'traits' in response.keys():
            self.traits = {key: (val[0]['value'], val[0]['confidence']) for key, val in response['traits'].items()}
        else:
            self.traits = None


a = wit('Remind me about my appointment tomorrow at 3pm')
print('Intent: ', a.intent)
print('Entities: ', a.entities)
print('Traits: ', a.traits)
