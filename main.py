import subprocess
import sys
import pprint
import word
import analysis

print(sys.argv)
if ("--" in sys.argv[1]):
    flag = str(sys.argv[1])[2:]
    words = sys.argv[2:]
else:
    flag = None
    words = sys.argv[1:]

print(words)
original = " ".join(words)

# Clean binary string and then create analysis structure to access contents
def clean(word):
    word = str(word)
    word = word[2:-5]
    word = word.replace("\\n", "\n")
    word = word.replace("\\r", "")
    word = word.replace("\\", "")
    list = [' '.join(x.split()) for x in word.split("\n")]

    return list

def analyze(word, f): # gives a word analysis of a singular word
    x = analysis.WordAnalysis(clean(word), f)
    return x.toString()

for word in words:
    proc = subprocess.check_output(f"bin/words {word}", shell=True)
    
    if(flag=="debug"):
        pprint.pprint(clean(proc))
  
    pprint.pprint(analyze(proc, flag)) # print word analysis cleanly
