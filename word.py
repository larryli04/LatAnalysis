class Word:
    def __init__(self):
        self.forms = []
        self.dict_entry = ""
        self.tags = ""
        self.definition = ""
        self.pos = ""

    def toString(self):
        return {
            "forms": self.forms,
            "dict_entry": self.dict_entry,
            "tags": self.tags,
            "definition": self.definition,
            "pos": self.pos
        }

class Noun(Word):
    def __init__(self):
        Word.__init__(self)
        self.case = []
        self.number = []
        self.gender = []
    def process(self, word):
        for item in word:
            self.forms.append(item.split(" ")[4:7])
        # case number gender
        for form in self.forms:
            self.case.append(form[0])
            self.number.append(form[1])
            self.gender.append(form[2])

class Adjective(Word):
    def __init__(self):
        Word.__init__(self)
        self.case = []
        self.number = []
        self.gender = []
        self.degree = []
    def process(self, word):
        for item in word:
            self.forms.append(item.split(" ")[4:8])
        # case number gender degree
        for form in self.forms:
            self.case.append(self.forms[0])
            self.number.append(self.forms[1])
            self.gender.append(self.forms[2])
            self.degree.append(self.forms[3])

class Verb(Word):
    def __init__(self):
        Word.__init__(self)
        
        self.tense = []
        self.voice = []
        self.mood = []
        self.person = []
        self.number = []
    def process(self, word):
        
        for item in word:
            self.forms.append(item.split(" ")[4:9])
        # tense voice mood person number
        
        for form in self.forms:
            self.tense.append(self.forms[0])
            self.voice.append(self.forms[1])
            self.mood.append(self.forms[2])
            self.person.append(self.forms[3])
            self.number.append(self.forms[4])
        
class Adverb(Word):
    def __init__(self):
        Word.__init__(self)
        self.degree = []
    def process(self, word):
        for item in word:
            self.forms.append(item.split(" ")[2])
        # degree
        for form in self.forms:
            self.degree.append(self.forms[0])

class Preposition(Word):
    def __init__(self):
        Word.__init__(self)
        self.plus = []
    def process(self, word):
        for item in word:
            self.forms.append(item.split(" ")[2])
        # the thing that it takes
        for form in self.forms:
            self.plus.append(self.forms[0])
