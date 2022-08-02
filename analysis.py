import word
import pprint

# WordAnalysis gives a structured breakdown of definition, forms, and other information

class WordAnalysis():
    def __init__(self, name, words, f):
        self.name = name
        self.words = []
        self.que = False
        #create a new word

        if("TACKON" in words[0]): # if there is a -que, to remove it from the Whitaker output
            words.pop(0)
            words.pop(0)
            self.que = True

        
        if(f == "debug"):
                pprint.pprint(words)
        
        while(len(words) != 0): # this should just delineate the three parts of Whitaker output, not put it into the class
            if(words[0]=="*"):
                break

            pos = words[0].split(" ")[1]
            chunk = []
            objects = []
            dict_entry = ""
            

            while(not "[" in words[0]):

                chunk.append(words.pop(0))

                if(pos == "ADJ"):
                    objects.append(word.Adjective())
                elif(pos == "N"):
                    objects.append(word.Noun())
                elif(pos == "ADV"):
                    objects.append(word.Adverb())
                elif(pos == "V"):
                    objects.append(word.Verb())
                elif(pos == "PREP"):
                    objects.append(word.Preposition())
                elif(pos == "PRON"):
                    objects.append(word.Noun())
                elif(pos == "VPAR"):
                    objects.append(word.Participle())
                else:
                    print("A word was not identified, try again")
                    exit()
            

            # while(not ";" in words[0]): # takes the last dictionary entry (why do we do this idk)
                
            dict_entry = words.pop(0)
            definition = []
            while(len(words)>0 and ";" in words[0]):
                definition.append(words.pop(0))

            for i in range(len(objects)):
                # print(words[0])
                currentWord = objects[i]
                currentWord.name = self.name
                if self.que == True:
                    currentWord.que = True

                currentWord.dict_entry = dict_entry
                currentWord.pos = pos # this
                
                
                currentWord.definition = definition
                currentWord.tags = [x for x in currentWord.dict_entry.split(" ") if ("[" in x)][0][1:-1]


                currentWord.process(chunk[i]) # process word-specifics like conjugations vs declensions
            
                self.append(currentWord) # add word to the Analysis 


            if(f == "debug"): # doesn't work right
                print("part of speech:", pos)
                print("chunk:", chunk)

            


            chunk = []
            objects = []

    def append(self, word):
        self.words.append(word)

    def toString(self):
        return [x.toString() for x in self.words] # doesn't include every data point in object

    def getVerbTenses(self): # common data point for deciding sentence structure OLD
        ans = []
        for word in self.words:

            if word.pos == "V":
                ans.append(word.tense)
        return ans
    
    def getNounCases(self): # common data point for deciding sentence structure OLD
        ans = []
        for word in self.words:

            if word.pos == "N":
                ans.append(word.case)
        return ans
