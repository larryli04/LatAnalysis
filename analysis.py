import word

# WordAnalysis gives a structured breakdown of definition, forms, and other information

class WordAnalysis():
    def __init__(self, words):
        self.words = []

        #create a new word
        
        while(len(words) != 0): # this should just delineate the three parts of Whitaker output, not put it into the class
            pos = words[0].split(" ")[1]
            if(pos == "ADJ"):
                currentWord = word.Adjective()
            elif(pos == "N"):
                currentWord = word.Noun()
            elif(pos == "ADV"):
                currentWord = word.Adverb()
            elif(pos == "V"):
                currentWord = word.Verb()
            elif(pos == "PREP"):
                currentWord = word.Preposition()
            else:
                print("A word was not identified, try again")
                exit()

            chunk = []

            currentWord.pos = pos # this

            while(not "[" in words[0]):
                chunk.append(words.pop(0))
                continue

            currentWord.dict_entry = words.pop(0) #maybe move these three into word.py
            currentWord.definition = words.pop(0)
            currentWord.tags = [x for x in currentWord.dict_entry.split(" ") if ("[" in x)][0][1:-1]

            currentWord.process(chunk) # process word-specifics like conjugations vs declensions
            
            self.append(currentWord) # add word to the Analysis

    def append(self, word):
        self.words.append(word)

    def toString(self):
        return [x.toString() for x in self.words] # doesn't include every data point in object

    def getVerbTenses(self): # common data point for deciding sentence structure
        ans = []
        for word in self.words:
            print(word.pos)
            if word.pos == "V":
                ans.append(word.tense)
        return ans
    
    def getNounCases(self): # common data point for deciding sentence structure
        ans = []
        for word in self.words:
            print(word.pos)
            if word.pos == "N":
                ans.append(word.case)
        return ans
