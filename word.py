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

class Pronoun(Word):
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
        self.gender = self.forms[2] # probably C
    

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
        self.inf = False
        self.tense = []
       
    def process(self, word):

        self.forms = word.split(" ")[4:9]

        # tense voice mood person number
        
        
        self.tense = self.forms[0]

        if(self.forms[2] == "INF"): # infinitive
            self.voice = self.forms[1]
            self.mood = self.forms[2]
            self.person = self.forms[3]
            self.number = self.forms[4]
        elif(len(self.forms) == 5): # regular verb
            self.voice = self.forms[1]
            self.mood = self.forms[2]
            self.person = self.forms[3]
            self.number = self.forms[4]
        
        elif(len(self.forms) == 4): # deponent
            self.voice = "ACTIVE"
            self.mood = self.forms[1]
            self.person = self.forms[2]
            self.number = self.forms[3]
        else:
            print("parsing the verbs went wrong")
        
    def toString(self):
        if (self.forms[2] == "INF"):
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
                "inf" : True

            }
        else:
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
    
class Participle(Word):
    def __init__(self):
        Word.__init__(self)
        
        self.tense = []
        self.voice = []
        self.person = []
        self.number = []
        self.gender = []
        self.case = []

    def process(self, word):

        self.forms = word.split(" ")[4:9]

        # tense voice mood person number
        print(self.forms)
        self.case = self.forms[0]
        self.number = self.forms[1]
        self.gender = self.forms[2]
        self.tense = self.forms[3]
        

        if(len(self.forms) == 5):
            self.voice = self.forms[4]
        
        elif(len(self.forms) == 4):
            self.voice = "ACTIVE"
        else:
            print("parsing the participle went wrong")

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
            "person" : self.person,
            "number": self.number

        }
    
class Adverb(Word):
    def __init__(self):
        Word.__init__(self)
        self.degree = []
    def process(self, word):

        self.forms = word.split(" ")[2]
        # degree
        # print(self.forms)
        
        self.degree = self.forms[0]

class Preposition(Word):
    def __init__(self):
        Word.__init__(self)
        self.plus = []
    def process(self, word):

        self.forms = word.split(" ")[2]
        # the thing that it takes
        # print(self.forms)

        self.plus = self.forms


        