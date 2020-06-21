from api_request import wit
from intent_handler import salutation, express, find, criticism, remind, correct, information

class conversation(wit):

    # inherts wit class in order to grab intent, entities, and traits
    def __init__(self, utter):
        super().__init__(utter)
        self.current_intent = None
        self.ongoing_intents = {}

    def update_utterance(self, utter):
        if self.current_intent is None:
            print('new topic')
            super().__init__(utter)
        else:
            print('continuing convo')
            super().__init__(utter, new_convo=False)
        # print('$$conversation updated$$')

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
        pass


if __name__ == '__main__':
    print('Person: Hey my name is Josh Stupidson')
    x = conversation('Hey my name is Josh Stupidson')
    print('Bot: ', x.parse_convo())

    x.update_utterance('Remind me to take my medicine in three minutes')
    print('Person: Remind me to take my medicine in three minutes')
    print('Bot: ', x.parse_convo())

    x.update_utterance('In 30 minutes')
    print('Person: In 30 minutes')
    print('Bot: ', x.parse_convo())
