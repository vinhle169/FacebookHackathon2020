from api_request import wit
from intent_handler import salutation, express, find, criticism, remind, correct, information

class conversation(wit):

    # inherts wit class in order to grab intent, entities, and traits
    def __init__(self, utter):
        print(f'Person: {utter}')
        super().__init__(utter)
        self.current_intent = None
        self.ongoing_intents = {}

    def update_utterance(self, utter):
        print(f'Person: {utter}')

        if self.current_intent is None:
            super().__init__(utter)
        else:
            super().__init__(utter, new_convo=False)
        print(self.entities)

    # runs the appropriate intent class
    def parse_convo(self):
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
        pass

    def find(self):
        pass

    def criticism(self):
        pass

    def remind(self):
        # add something to save datetime and reminder details
        if 'remind' not in self.ongoing_intents:
            self.ongoing_intents['remind'] = remind(self.entities, self.traits)
            self.ongoing_intents['remind'].generate_response()
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
            self.current_intent = None
        else:
            self.ongoing_intents['info'].generate_response(new_ent=self.entities, new_trait=self.traits)
            self.current_intent = None
        return self.ongoing_intents['info'].response


if __name__ == '__main__':
    x = conversation('Hey my name is Vincent Vangough')
    print('Bot: ', x.parse_convo(), '\n')

    x.update_utterance('Remind me to take my medicine in 2 hours')
    print('Bot: ', x.parse_convo(), '\n')

    x.update_utterance('In 30 minutes')
    print('Bot: ', x.parse_convo(), '\n')

    x.update_utterance('remind me to walk the dogs every 20 hours')
    print('Bot:', x.parse_convo(), '\n')

    x.update_utterance('tell me about recent covid stats')
    print('Bot:', x.parse_convo(), '\n')

    x.update_utterance('I think i have a family member with corona')
    print('Bot:', x.parse_convo(), '\n')

    x.update_utterance('What are the symptoms of corona?')
    print('Bot:', x.parse_convo(), '\n')
    x.update_utterance('What can I find online about the flu?')
