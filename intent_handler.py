import re
import json
import requests
from random import randint
from datetime import datetime
from bs4 import BeautifulSoup
from googlesearch import search
class main_intent:

    def __init__(self, entities, traits):
        self.entities = entities
        self.traits = traits
        self.new = True
        self.response = "I'm not sure what are you saying can you try rephrasing that"
        self.current_time = datetime.now()
        self.g_api_key = 'AIzaSyCE3wsY5xE41YPGVQavGq0EyVD1lo1b44Q'

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

    def emotion_handler(self, emotion):
        if emotion == 'happy':
            self.response = "YESSS we love to hear that :D"
        else:
            with open('response.json', 'r') as jk:
                resp = json.load(jk)
            if emotion == 'sad':
                resp = resp["jokes"]
                self.response = f"{resp['0']}{resp[str(randint(1,3))]}"
            else:
                self.response = resp["corona"][emotion]

    def generate_response(self, new_ent=None, new_trait=None):
        if new_ent:
            self.entities = new_ent
        if new_trait:
            self.trait = new_trait

        if 'emotion' in self.entities:
            emote = self.entities['emotion']['role']
            self.emotion_handler(emote)

        elif 'symptom' in self.entities:
            simp = self.entities['symptom']
            body_parts = simp.get('body_part')
            body_part = body_parts['val'] if body_parts else ''
            symps = simp.get('symptom') or simp.get('specific')
            symp = symps['val']
            q = body_part + ' ' + symp
            q1, q2 = q + ' information', q + ' treatment'
            q1 = f"Here's some information on {q} " + [i for i in search(q1, tld="com", num=1, stop=1, pause=.5)][0]
            q2 = f"Here's info on how to treat {q} " + [i for i in search(q2, tld="com", num=1, stop=1, pause=.5)][0]
            self.response = f"{q1}\n{q2}\nHope this helps!"
        self.new = True

class find(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)
        self.curr_location, self.end_location = None, None

    def generate_response(self, new_ent=None, new_trait=None):
        if new_ent:
            self.entities = new_ent
        if new_trait:
            self.trait = new_trait

        def search_info(query):
            goal = [i for i in search(query + ' info', tld="com", num=1, stop=1, pause=1)][0]
            self.response = f'You should check out {goal}, hope this is helpful!'
            self.new = True

        if 'topic' in self.entities:
            search_info(self.entities['topic']['val'])

        elif 'facilities' in self.entities:
            if self.entities['facilities']['role'] != 'facilities':
                self.end_location = self.entities['facilities']['role']
            else:
                self.end_location = self.entities['facilities']['val']
            self.response = f"Where are you trying to reach the {self.end_location} from? I want to tell you the nearest one."
            self.new = False
        elif 'wit$location' in self.entities:
            self.curr_location = self.entities['wit$location']['val']
            url = "https://maps.googleapis.com/maps/api/place/textsearch/json?"
            r = requests.get(url + 'query=' + self.end_location + '&open' + '&key=' + self.g_api_key)
            result = r.json()['results'][0]
            address = result['formatted_address']
            name = result['name']
            self.new = True
            self.response = f"{name} at {address} is the closest open place to the location you provided"

class criticism(main_intent):

    def __init__(self, entities, traits):
        super().__init__(entities, traits)
        self.review = set()

    def generate_response(self, utter):
        self.review.add((utter, datetime.now()))
        if 'wit$sentiment' in self.traits:
            if self.traits['wit$sentiment'][0] != 'negative':
                self.response = "Thank you for the kind words you're amazing c:"
                self.new = True
                return True
            else:
                self.response = "Sorry you feel that way would you like to tell us more?"
        else:
            self.response = "Okay, would you like to tell us more?"
        self.new = False
        return False

    def more_criticism(self, utter):
        if 'no' in utter.lower():
            self.response = "That's okay sorry the bot isn't perfect yet, we will take your words into consideration"
        else:
            self.review.add((utter, datetime.now()))
            self.response = "Ok noted, thank you we will check this out ASAP"
        self.new = True

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
                self.new = True
            else:
                self.response = f"When would you want us to remind you about '{self.reminder}'?"
                self.new = False
        elif 'wit$datetime' in self.entities:
            date, time = self.entities['wit$datetime']['val'].split('T')
            time = time[:time.find('-')]
            self.datetime_obj = datetime.strptime(' '.join([date, time]), '%Y-%m-%d %H:%M:%S.%f')
            x = self.datetime_obj.strftime("on %m-%d-%Y at %H:%M")
            self.response = f"Ok got it, you will be reminded about '{self.reminder}' {x}"
            self.new = True

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
            self.new = True
        elif 'health' in self.entities:
            role = self.entities['health']['role']
            with open('response.json', 'r') as cr:
                health_responses = json.load(cr)["health"]
            self.response = health_responses[role]
            self.new = True

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
