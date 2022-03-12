import word

# WordAnalysis gives a structured breakdown of definition, forms, and other information

class WordAnalysis():
    def __init__(self, words):
        self.words = []

        #create a new word
        currentWord = word.Word()
        chunk = []
        while(len(words) != 0): # this should just delineate the three parts of Whitaker output, not put it into the class
            currentWord.pos = words[0].split(" ")[1]
            while(not "[" in words[0]):
                chunk.append(words.pop(0))
                continue
            currentWord.dict_entry = words.pop(0) #maybe move these three into word.py
            currentWord.definition = words.pop(0)
            currentWord.tags = [x for x in currentWord.dict_entry.split(" ") if ("[" in x)][0][1:-1]

            currentWord.process(chunk) # process word-specifics like conjugations vs declensions
            chunk = []
            
            self.append(currentWord)
            currentWord = word.Word()

            print(self.words)

    def append(self, word):
        self.words.append(word)

    def allForms(self):
        temp = []
        for word in self.words:
            temp.append(word.forms)
        return temp


    def toString(self):
        return [x.toString() for x in self.words]