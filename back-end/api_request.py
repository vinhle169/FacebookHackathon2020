#import requests
import eventlet

eventlet.patcher.import_patched("requests")

# class to handle the return of a get call to the wit api when given an utterance
class wit:

    def __init__(self, utter, new_convo=True):
        self.utterance = utter
        URL = f'https://api.wit.ai/message?v=20200615&q={self.utterance}'
        self.server_Token = 'XHAXSXINWBD5KFLNDL5AQWXO4O7672EC'
        self.auth_Header = {'Authorization': f'Bearer {self.server_Token}'}
        response = requests.get(url=URL, headers=self.auth_Header).json()
        if new_convo:
            if 'intents' not in response or len(response['intents']) == 0:
                self.intent, self.entities, self.traits = None, None, None
                return
            self.intent = response['intents'][0]['name']
        # entities are stored as {entity_name: {val: entity_value, conf: entity: confidence, role: entity_role}, entity_2: {...}...}
        self.entities = {}
        special_cases = {'wit$duration', 'resources', 'wit$location', 'symptom'}
        for val in response['entities'].values():
            val = val[0]
            name = val['name']
            if name not in special_cases:
                self.entities[name] = {'val': val['value'], 'conf': val['confidence'], 'role': val['role']}
            elif name == 'symptom':
                self.entities.setdefault(name, {})
                self.entities[name][val['role']] = {'val': val['value']}
            elif name == 'wit$location':
                if 'value' in val:
                    self.entities[name] = {'val': val['value'], 'conf': val['confidence'], 'role': val['role']}
                else:
                    self.entities[name] = {'val': val['resolved']['values'][0]['name'], 'conf': val['confidence'], 'role': val['role']}
            elif name == 'wit$duration':
                self.entities[name] = {'val': val['body'], 'conf': val['confidence'],
                                       'role': val['role'], 'seconds': val['normalized']['value']}
            elif name == 'resources':
                self.entities[val['role']] = {'val': val['value'], 'conf': val['confidence']}
        # traits are stored as {trait: (val, confid)}
        if 'traits' in response.keys():
            self.traits = {key: (val[0]['value'], val[0]['confidence']) for key, val in response['traits'].items()}
        else:
            self.traits = None
