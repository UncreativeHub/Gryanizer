"""
Add a letter to a name to make a new one
"""

from typing import List,Dict,Tuple
import random

SDICT = "data/csw19.txt" #list of words one per line
NAMESOURCE = "data/player_names.txt" #format for each row: "id<TAB>first name<TAB>last name"
OUTPUTPATH = "output/gryanized.txt" #output

ALPHABET = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

#Analyze english word dyad frequency
dyadKeys: List[str] = []
words: List[str] = []
for c1 in ALPHABET:
    for c2 in ALPHABET:
        dyadKeys.append(f"{c1}{c2}")

dyadFreq: Dict[str,int] = dict.fromkeys(dyadKeys,0)

with open(SDICT) as WORDFILE:
    words = WORDFILE.readlines()
    words = [w.replace("\n","") for w in words]

    WORDFILE.close()

dyadTotal = 0
for w in words:
    for i in range(0,len(w) - 1):
        ss = w[i:i+2]
        dyadFreq[ss] += 1
        dyadTotal += 1

#triads
triadKeys: List[str] = []
for c1 in ALPHABET:
    for c2 in ALPHABET:
        for c3 in ALPHABET:
            triadKeys.append(f"{c1}{c2}{c3}")

triadFreq: Dict[str,int] = dict.fromkeys(triadKeys,0)

triadTotal = 0
for w in words:
    for i in range(0,len(w)-2):
        ss = w[i:i+3]
        triadFreq[ss] += 1
        triadTotal += 1
        
triadMultiplier = dyadTotal/triadTotal
for k in triadFreq.keys():
    triadFreq[k] *= triadMultiplier

#load players
players: Dict[str,Tuple[str,str]] = dict()
newPlayers: Dict[str,Tuple[str,str]] = dict()

with open(NAMESOURCE) as NAMESOURCEFILE:
    pnLines = NAMESOURCEFILE.readlines()
    for line in pnLines:
        toks = line[:-1].split("\t")
        players[toks[0]] = (toks[1].split(" ")[0].upper(),toks[2].upper())

modPlayers: List[Tuple[str,str]] = []
for p in players.keys():
    fName = players[p][0]

    potents = []
    weights = []
    for i in range(0,len(fName) + 1):
        potents += [(i,c) for c in ALPHABET]

    for pot in potents:
        freqs = []
        i = pot[0]
        #dyad
        if i != len(fName):
            freqs.append(dyadFreq[f"{pot[1]}{fName[i]}"])
        
        if i != 0:
            freqs.append(dyadFreq[f"{fName[i-1]}{pot[1]}"])

        #triad
        nSets = [(i-1,i,None),(i-1,None,i),(None,i,i+1)]
        nSets = [n for n in nSets if -1 not in n and len(fName) not in n]
        for n in nSets:
            key = ""
            for j in n:
                if isinstance(j,int):
                    key += fName[j]
                else:
                    key += pot[1]
            
            freqs.append(triadFreq[key])
        
                    

        odds = sum(freqs)/len(freqs)
        weights.append(odds)

    potSel = random.choices(potents,weights)[0]
    newfName = fName[:potSel[0]] + potSel[1] + fName[potSel[0]:]

    newPlayers[p] = (newfName,players[p][1])

outStr = ""
for p in players.keys():
    outStr += f"{p}: {players[p][0]} {players[p][1]} - {newPlayers[p][0]} {newPlayers[p][1]}\n"

with open(OUTPUTPATH,"w") as GRYANIZED:
    GRYANIZED.write(outStr)
    GRYANIZED.close()