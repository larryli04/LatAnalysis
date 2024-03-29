import subprocess
import sys
import pprint
import word
import analysis



# Clean binary string and then create analysis structure to access contents
def clean(word):

    word = word.decode("utf-8") 
    # print(word)
    # word = word.replace("\\n", "\n")

    word = word.replace("\r", "")

    word = word.replace("\\", "")

    word = word.rstrip("\n")

    list = [' '.join(x.split()) for x in word.split("\n")]
    # print(list)

    return list

def analyze(word,wordput, f): # gives a word analysis of a singular word
    x = analysis.WordAnalysis(word, clean(wordput), f)

    # return x.toString()
    return x

if __name__ == "__main__":
    w = sys.argv[1]

    p = subprocess.Popen(["bin/words",f"{w}"], stdin=subprocess.PIPE, stdout=subprocess.PIPE)
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
        if(b'Syncope' in pline):
            pline = p.stdout.readline()
            pline = p.stdout.readline()
        
    
    proc = b"".join(proc)
    pprint.pprint(clean(proc))
    pprint.pprint(analyze(w, proc, None).toString()) # print word analysis cleanly

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
        if(b'Syncope' in pline):
            pline = p.stdout.readline()
            pline = p.stdout.readline()
        
    
    proc = b"".join(proc)

    # pprint.pprint(clean(proc))
    return analyze(word,proc, None)