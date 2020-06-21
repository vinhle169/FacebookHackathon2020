import re
import json
import requests
from datetime import datetime
from bs4 import BeautifulSoup

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
        if 'wit$greetings' in self.traits and 'wit$bye' in self.traits:
            if self.traits['wit$greetings'][1] >= self.traits['wit$bye'][1]:
                del self.traits['wit$bye']
            else:
                del self.traits['wit$greetings']
        if 'wit$greetings' in self.traits:
            self.response = 'Whatsup!'
            if 'wit$contact' in self.entities:
                self.response = f"{self.response[:-1]} {self.entities['wit$contact']['val']}!"
        elif 'wit$bye' in self.traits:
            self.response = 'Cya!'


class express(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class find(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self, new_ent, new_trait):
        if new_ent:
            self.entities = new_ent
        if new_trait:
            self.trait = new_trait

        def search(query, online=True):
            pass
        if 'topic' in self.entities:
            search(self.entities['topic']['val'], online='online' in self.entities)
        


class criticism(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class remind(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)
        self.datetime_obj, self.reminder, self.interval = None, None, None

    def generate_response(self, new_ent=None, new_trait=None):

        if new_ent:
            self.entities = new_ent
        if new_trait:
            self.trait = new_trait
        if 'wit$reminder' in self.entities:
            self.reminder = self.entities['wit$reminder']['val']
            if 'wit$duration' in self.entities:
                self.interval = self.entities['wit$duration']['seconds']
                self.response = f"Ok got it, you will be reminded about {self.reminder} every {self.entities['wit$duration']['val']}"
            else:
                self.response = f"When would you want us to remind you about '{self.reminder}'?"

        elif 'wit$datetime' in self.entities:
            date, time = self.entities['wit$datetime']['val'].split('T')
            time = time[:time.find('-')]
            self.datetime_obj = datetime.strptime(' '.join([date, time]), '%Y-%m-%d %H:%M:%S.%f')
            x = self.datetime_obj.strftime("on %m-%d-%Y at %H:%M")
            self.response = f"Ok got it, you will be reminded about '{self.reminder}' {x}"


class correct(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self):
        pass

class information(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)

    def generate_response(self, new_ent=None, new_trait=None):

        if new_ent:
            self.entities = new_ent
        if new_trait:
            self.trait = new_trait

        if 'rona' in self.entities:
            role = self.entities['rona']['role']
            if role == 'rona':
                self.webcrawl('rona')
            else:
                with open('response.json', 'r') as cr:
                    rona_responses = json.load(cr)["corona"]
                self.response = rona_responses[role]
        elif 'health' in self.entities:
            role = self.entities['health']['role']
            with open('response.json', 'r') as cr:
                health_responses = json.load(cr)["health"]
            self.response = health_responses[role]

    def webcrawl(self, u):
        if u == 'rona':
            url = "https://www.cdc.gov/coronavirus/2019-ncov/cases-updates/cases-in-us.html"
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            stats = soup.findAll("div", class_="callout")
            target = stats[0].get_text().lower()
            target = re.findall("[a-zA-Z\b\d+\b,]+", target)
            target2 = stats[1].get_text().lower()
            target2 = re.findall("[a-zA-Z\b\d+\b,]+", target2)
            self.response = "Recent statistics state that there are "
            string1 = f"{' '.join(target[2::-1])} and within 24 hours there were {' '.join(target[3:])}.\n"
            string2 = f"Sadly the total death count is {target2[2]} and there were {' '.join(target2[3:])} yesterday."
            self.response += string1 + string2
        else:
            pass
            return None
