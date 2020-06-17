import requests

# class to handle the return of a get call to the wit api when given an utterance
class wit:

    def __init__(self, utter, new_convo=True):
        self.utterance = utter
        URL = f'https://api.wit.ai/message?v=20200615&q={self.utterance}'
        self.server_Token = 'XHAXSXINWBD5KFLNDL5AQWXO4O7672EC'
        self.auth_Header = {'Authorization': f'Bearer {self.server_Token}'}
        response = requests.get(url=URL, headers=self.auth_Header).json()
        # print(response)
        if new_convo:
            self.intent = response['intents'][0]['name']
            if len(response['intents']) == 0:
                print("Unexpected no intent")
                raise
        self.entities = {val[0]['name']: {'val': val[0]['value'], 'conf': val[0]
                                          ['confidence'], 'role': val[0]['role']} for val in response['entities'].values()}

        if 'traits' in response.keys():
            self.traits = {key: (val[0]['value'], val[0]['confidence']) for key, val in response['traits'].items()}
        else:
            self.traits = None

