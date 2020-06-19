from datetime import datetime

class main_intent:

    def __init__(self, entities, traits):
        self.entities = entities
        self.traits = traits
        self.response = "I'm not sure what are you saying can you try rephrasing that"
        self.current_time = datetime.now()

class salutation(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        if 'wit$greetings' in self.traits:
            self.response = 'Wassup'
        elif 'wit$bye' in self.traits:
            self.response = 'Cya'
        if 'wit$contact' in self.entities:
            self.response += f" {self.entities['wit$contact']['val']}"

class express(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class find(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class criticism(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class remind(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)
        self.datetime_obj, self.action_to_take = None, None

    def generate_response(self, new_ent=None, new_trait=None):

        if new_ent:
            self.entities = new_ent
        if new_trait:
            self.trait = new_trait

        if 'wit$reminder' in self.entities:
            self.action_to_take = self.entities['wit$reminder']['val']
            self.response = f"When would you want us to remind you about '{self.action_to_take}'?"

        elif 'wit$datetime' in self.entities:
            date, time = self.entities['wit$datetime']['val'].split('T')
            time = time[:time.find('-')]
            self.datetime_obj = datetime.strptime(' '.join([date, time]), '%Y-%m-%d %H:%M:%S.%f')
            x = self.datetime_obj.strftime("%m-%d-%Y %H:%M")
            self.response = f"Ok got it, you will be reminded about '{self.action_to_take}' in {x}"

        elif 'wit$duration' in self.entities:
            self.response = f"Ok got it, you will be reminded about {self.action_to_take} in "


class correct(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class information(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass
