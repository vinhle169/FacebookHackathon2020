import requests

# class to handle the return of a get call to the wit api when given an utterance
class wit:

    def __init__(self, utter):
        self.utterance = utter
        URL = f'https://api.wit.ai/message?v=20200615&q={self.utterance}'
        server_Token = 'XHAXSXINWBD5KFLNDL5AQWXO4O7672EC'
        auth_Header = {'Authorization': f'Bearer {server_Token}'}
        response = requests.get(url=URL, headers=auth_Header).json()

        self.intent = response['intents'][0]['name']
        self.entities = {val[0]['name']: {'val': val[0]['value'], 'conf': val[0]
                                          ['confidence'], 'role': val[0]['role']} for val in response['entities'].values()}

        if 'traits' in response.keys():
            self.traits = {key: (val[0]['value'], val[0]['confidence']) for key, val in response['traits'].items()}
        else:
            self.traits = None
