import subprocess
import sys
import pprint
import word
import analysis

words = sys.argv[1:]
original = " ".join(words)

# Clean binary string and then create analysis structure to access contents
def clean(word):
    word = str(word)
    word = word[2:-5]
    word = word.replace("\\n", "\n")
    word = word.replace("\\r", "")
    list = [' '.join(x.split()) for x in word.split("\n")]

    return list

def analyze(word): # gives a word analysis of a singular word
    x = analysis.WordAnalysis(clean(word))
    return x.toString()

for word in words:
    proc = subprocess.check_output(f"bin/words {word}", shell=True)
    
    pprint.pprint(analyze(proc)) # print word analysis cleanly
