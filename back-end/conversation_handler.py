from api_request import wit
from intent_handler import salutation, express, find, criticism, remind, information

class conversation(wit):

    # inherts wit class in order to grab intent, entities, and traits
    def __init__(self, utter):
        print(f'Person: {utter}')
        super().__init__(utter)
        self.current_intent = None
        self.thanks = {'thanks', 'thank you', 'much appreciated'}
        self.ongoing_intents = {}
        self.criticisms = set()
        self.unknown_response = "I am sorry can you try rephrasing that, I might not be built to handle your request"

    def update_utterance(self, utter):
        print(f'Person: {utter}')

        if self.current_intent is None:
            super().__init__(utter)
        else:
            super().__init__(utter, new_convo=False)
        # print(self.entities)

    # runs the appropriate intent class
    def parse_convo(self):
        if self.utterance.lower() in self.thanks:
            return "No problem! Glad to be of service (◕‿◕✿)"
        if not self.intent and not self.current_intent:
            self.current_intent = None
            return self.unknown_response
        intent = getattr(self, self.intent)
        self.current_intent = intent
        return self.current_intent()

    # below are the list of methods which run the appropriate classes
    def salutation(self):
        # add something in the future to save name if name is sent
        s = salutation(self.entities, self.traits)
        s.generate_response()
        self.current_intent = None
        return s.response

    def express(self):
        self.ongoing_intents.setdefault('express', express(self.entities, self.traits))
        self.ongoing_intents['express'].generate_response(self.entities, self.traits)
        self.current_intent = None
        return self.ongoing_intents['express'].response

    def find(self):
        if 'find' not in self.ongoing_intents or self.ongoing_intents['find'].new:
            self.ongoing_intents['find'] = find(self.entities, self.traits)
            self.ongoing_intents['find'].generate_response()
            if self.ongoing_intents['find'].new:
                self.current_intent = None
        else:
            self.ongoing_intents['find'].generate_response(new_ent=self.entities, new_trait=self.traits)
            self.current_intent = None
        return self.ongoing_intents['find'].response

    def criticism(self):
        if 'criticism' not in self.ongoing_intents or self.ongoing_intents['criticism'].new:
            self.ongoing_intents['criticism'] = criticism(self.entities, self.traits)
            self.current_intent = None if self.ongoing_intents['criticism'].generate_response(self.utterance) else self.current_intent
        else:
            self.ongoing_intents['criticism'].more_criticism(self.utterance)
            self.current_intent = None
        self.criticisms.union(self.ongoing_intents['criticism'].review)
        return self.ongoing_intents['criticism'].response

    def remind(self):
        # add something to save datetime and reminder details
        if 'remind' not in self.ongoing_intents or self.ongoing_intents['remind'].new:
            self.ongoing_intents['remind'] = remind(self.entities, self.traits)
            self.ongoing_intents['remind'].generate_response()
            if self.ongoing_intents['remind'].new:
                self.current_intent = None
        else:
            self.ongoing_intents['remind'].generate_response(new_ent=self.entities, new_trait=self.traits)
            self.current_intent = None
        return self.ongoing_intents['remind'].response

    def correct(self):
        pass

    def information(self):
        if 'info' not in self.ongoing_intents:
            self.ongoing_intents['info'] = information(self.entities, self.traits)
            self.ongoing_intents['info'].generate_response()
        else:
            self.ongoing_intents['info'].generate_response(new_ent=self.entities, new_trait=self.traits)
        self.current_intent = None
        return self.ongoing_intents['info'].response


if __name__ == '__main__':
    pass
