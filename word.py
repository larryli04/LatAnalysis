class Word:
    def __init__(self):
        self.name = ""
        self.forms = []
        self.dict_entry = ""
        self.tags = ""
        self.definition = ""
        self.pos = ""
        self.que = False

    def toString(self):
        return {
            "name": self.name,
            "forms": self.forms,
            "dict_entry": self.dict_entry,
            "tags": self.tags,
            "definition": self.definition,
            "pos": self.pos,
            "que": self.que
        }

class Noun(Word):
    def __init__(self):
        Word.__init__(self)
        self.case = []
        self.number = []
        self.gender = []
    def process(self, word):
        self.forms = word.split(" ")[4:7]
        # case number gender

        self.case = self.forms[0]
        self.number = self.forms[1]
        self.gender = self.forms[2]
    def toString(self):
        return {
            "name": self.name,
            "forms": self.forms,
            "dict_entry": self.dict_entry,
            "tags": self.tags,
            "definition": self.definition,
            "pos": self.pos,
            "que": self.que,
            "case": self.case,
            "number": self.number,
            "gender": self.gender
        }

class Adjective(Word):
    def __init__(self):
        Word.__init__(self)
        self.case = []
        self.number = []
        self.gender = []
        self.degree = []
    def process(self, word):

        self.forms = word.split(" ")[4:8]
        # print(self.forms)
        # case number gender degree

        self.case = self.forms[0]
        self.number = self.forms[1]
        self.gender = self.forms[2]
        self.degree = self.forms[3]
    def toString(self):
        return {
            "name": self.name,
            "forms": self.forms,
            "dict_entry": self.dict_entry,
            "tags": self.tags,
            "definition": self.definition,
            "pos": self.pos,
            "que": self.que,
            "case": self.case,
            "number": self.number,
            "gender": self.gender,
            "degree": self.degree
        }

class Verb(Word):
    def __init__(self):
        Word.__init__(self)
        
        self.tense = []
        self.voice = []
        self.mood = []
        self.person = []
        self.number = []
    def process(self, word):

        self.forms = word.split(" ")[4:9]

        # tense voice mood person number
        # print(self.forms)

        self.tense = self.forms[0]
        self.voice = self.forms[1]
        self.mood = self.forms[2]
        self.person = self.forms[3]
        self.number = self.forms[4]
    def toString(self):
        return {
            "name": self.name,
            "forms": self.forms,
            "dict_entry": self.dict_entry,
            "tags": self.tags,
            "definition": self.definition,
            "pos": self.pos,
            "que": self.que,
            "tense" : self.tense,
            "voice" : self.voice,
            "mood" : self.mood,
            "person" : self.person,
            "number": self.number

        }
    
class Adverb(Word):
    def __init__(self):
        Word.__init__(self)
        self.degree = []
    def process(self, word):
        for item in word:
            self.forms.append(item.split(" ")[2])
        # degree
        # print(self.forms)
        for form in self.forms:
            self.degree.append(form[0])

class Preposition(Word):
    def __init__(self):
        Word.__init__(self)
        self.plus = []
    def process(self, word):
        for item in word:
            self.forms.append(item.split(" ")[2])
        # the thing that it takes
        # print(self.forms)
        for form in self.forms:
            self.plus.append(form[0])
