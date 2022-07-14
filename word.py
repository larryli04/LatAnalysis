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
        for item in word:
            self.forms.append(item.split(" ")[4:7])
        # case number gender
        for form in self.forms:
            self.case.append(form[0])
            self.number.append(form[1])
            self.gender.append(form[2])
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
        for item in word:
            self.forms.append(item.split(" ")[4:8])
        # print(self.forms)
        # case number gender degree
        for form in self.forms:
            self.case.append(form[0])
            self.number.append(form[1])
            self.gender.append(form[2])
            self.degree.append(form[3])
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
        
        for item in word:
            self.forms.append(item.split(" ")[4:9]) # changed this but maybe not from = to append

        # tense voice mood person number
        # print(self.forms)
        for form in self.forms:
            self.tense.append(form[0])
            self.voice.append(form[1])
            self.mood.append(form[2])
            self.person.append(form[3])
            self.number.append(form[4])
    
    
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
