import subprocess
import sys
import pprint
import word
import analysis



# Clean binary string and then create analysis structure to access contents
def clean(word):

    word = word.decode("utf-8") 
    word = word.replace("\\n", "\n")
    word = word.replace("\\r", "")
    word = word.replace("\\", "")
    word = word.rstrip("\n")
    list = [' '.join(x.split()) for x in word.split("\n")]

    return list

def analyze(word,wordput, f): # gives a word analysis of a singular word
    x = analysis.WordAnalysis(word, clean(wordput), f)
    return x.toString()

if __name__ == "__main__":
    print(sys.argv)
    if ("--" in sys.argv[1]):
        flag = str(sys.argv[1])[2:]
        words = sys.argv[2:]
    else:
        flag = None
        words = sys.argv[1:]

    print(words)
    original = " ".join(words)

    for w in words:
        proc = subprocess.check_output(f"bin/words {w}", shell=True)
        
        if(flag=="debug"):
            pprint.pprint(clean(proc))
    
        pprint.pprint(analyze(w, proc, flag)) # print word analysis cleanly

def getWhitakers(word): # function that gets the parsed whitaker's output of a single word
    # proc = subprocess.check_output(f"bin/words {word}", shell=True)
    p = subprocess.Popen(["bin/words",f"{word}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
    proc = []
    pline = p.stdout.readline()

    while(len(pline) != 0):
        if(pline == b"*\n"):
            break
        proc.append(pline)

        pline = p.stdout.readline()

        if(b"MORE - hit RETURN/ENTER to continue" in pline):

            p.stdin.write('\n'.encode('utf-8'))
            p.stdin.flush() # i don't know what this does but it makes stdin work
            pline = p.stdout.readline()
        
    
    proc = b"".join(proc)

    # pprint.pprint(clean(proc))
    return analyze(word,proc, None)