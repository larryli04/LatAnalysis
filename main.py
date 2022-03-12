import subprocess
import sys
import json
import pprint
import word
import analysis

words = sys.argv[1:]
original = " ".join(words)


# considering this structure to better analyze possibilities

# forms = {
#         "N": {},
#         "V": {},
#         "ADJ": {},
#         "ADV": {},
#         "PREP": {}
# }


# Clean binary string and then create analysis structure to access contents
def clean(word):
    word = str(word)
    word = word[2:-5]
    word = word.replace("\\n", "\n")
    list = [' '.join(x.split()) for x in word.split("\n")]

    return list

def forms(word):
    x = analysis.WordAnalysis(word)
    return x.toString()


for word in words:
    proc = subprocess.check_output(f"bin/words {word}", shell=True)
    # print(definition(clean(proc)))
    pprint.pprint(forms(clean(proc)))
    # print(cases(forms(clean(proc))))

