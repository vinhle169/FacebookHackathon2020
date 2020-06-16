from api_request import wit


class conversation(wit):

    # inherts wit class in order to grab intent, entities, and traits
    def __init__(self, utter):
        super().__init__(utter)


    # runs the appropriate intent class
    def parse_convo(self):
        intent = getattr(self, self.intent)
        return intent()

    # below are the list of methods which run the appropriate classes
    def salutation(self):
        s = salutation(self.entities, self.traits)
        s.generate_response()
        return s.response

    def express(self):
        pass

    def find(self):
        pass

    def criticism(self):
        pass

    def remind(self):
        pass

    def correct(self):
        pass

class main_intent:

    def __init__(self, entities, traits):
        self.entities = entities
        self.traits = traits

class salutation(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        self.response = 'Wassup'
        if 'name' in self.entities:
            self.response += f" {self.entities['name']['val']}"


x = conversation('Hello my name is Joshua Fajardo')
print(x.parse_convo())
