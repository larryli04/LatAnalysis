from re import L


class Word:

    def __init__(self):
        self.forms = []
        self.dict_entry = ""
        self.tags = ""
        self.definition = ""
        self.pos = ""

        # while(not "[" in words[0]):
        #     if(self.pos == "ADJ"): # different information for each part of speech
        #         self.forms.append(words.pop(0).split(" ")[-4:])
        #     if(self.pos == "N"):
        #         self.forms.append(words.pop(0).split(" ")[-3:])
            # self.dict_entry = words.pop(0)
            # self.definition = words.pop(0)
            # self.tags = [x for x in self.dict_entry.split(" ") if ("[" in x)][0][1:-1]


    def process(self, word): # this is one word
        print("WORD",word)
        for item in word:
            if(self.pos == "ADJ"): # different information for each part of speech
                self.forms.append(item.split(" ")[4:8])
            if(self.pos == "N"):
                self.forms.append(item.split(" ")[4:7])
            if(self.pos == "V"):
                self.forms.append(item.split(" ")[4:9])
            if(self.pos == "PREP"):
                self.forms.append(item.split(" ")[1:3])

    def toString(self):
        return {
            "forms": self.forms,
            "dict_entry": self.dict_entry,
            "tags": self.tags,
            "definition": self.definition,
            "pos": self.pos
        }

class Noun(Word):
    def process(self, word): # this is one word
        for item in word:
            if(self.pos == "N"):
                self.forms.append(item.split(" ")[4:7])

            

