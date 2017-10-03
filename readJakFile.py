#!/usr/bin/python3
import sys
from collections import Counter, defaultdict


def readStopWords(fname):
    f = open(fname)
    swd = {}
    for line in f.readlines():
        swd[line.strip().lower()] = 1
    print('read in', len(swd),'from', fname)
    #print(swd)
    return swd

def readNameGroups(fname):
    f = open(fname)
    ngs = []
    for line in f.readlines():
        ngs.append(line.strip().lower().split(':'))
    print('read in', len(ngs), 'from', fname)
    print(ngs)
    return ngs

stopWords = readStopWords('stopWords.txt')
nameGroups = readNameGroups('manualGroups.txt')
names = Counter()
for ng in nameGroups:
    for name in ng:
        names[name]+=1

print('names:', names)

def editDist(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def isRec(line):
    if len(line)==0 or line[0].isspace() or not line[0].isdigit():
        return 0
    return True

sheetLines = []
class SheetLine:
    def __init__(self, line):
        self.sp = line.strip('\n\r').split('\t')

for line in sys.stdin:
    if isRec(line):
        sline = SheetLine(line)
        if len(sline.sp)>4:
            sheetLines.append(sline)

print("found", len(sheetLines), 'lines')

def findLastNames(line):
    #print('line:', line)
    lnames = []
    pos = 0
    length = len(line)
    #curName = ''
    inName = 0
    while pos < length:
        if line[pos].isupper():
            curName = ''
            while pos<length and line[pos].isupper():
                curName = curName + line[pos]
                pos = pos+1
            if len(curName)>1 and not curName in ['NO', 'LAST', 'NAME']:
                lnames.append(curName.lower())
        pos = pos+1
    #print('lnames:', lnames)
    return lnames

def findNames(line):
    names = []
    pos = 0
    length = len(line)
    inName = 0
    while pos < length:
        if line[pos].isalpha():
            curName = ''
            while pos<length and line[pos].isalpha():
                curName += line[pos].lower()
                pos += 1
            if len(curName)>1 and not curName in stopWords:
                names.append(curName)
        if line[pos]=='(':  # skip parentheticals
            while pos<length and line[pos]!=')':
                pos += 1
        pos += 1
    return names

for sline in sheetLines:
    for name in findNames('\t'.join(sline.sp)):
        # if len(names)<50:
        #     print(name, ':', ' '.join(sline.sp))
        names[name] += 1

print('found %d different names'% len(names))

def putInGroup(name, group):
    if name in group:
        return 0
    matchCount = 0
    dbg = 0#name in ['orina']
    if dbg:
         print('checking', name, 'against', group)
    minDist = len(name)
    for gname in group:
        eD = editDist(name, gname)
        minDist = min(minDist, eD)
        if eD<=2:
            matchCount += 1
    goodMatch = minDist==1 or matchCount>(len(group)+1)//2
    # if dbg:
    #     print('minDist', minDist, 'matchCount=', matchCount, 'group length', len(group))
    #     print('', 'goodMatch', goodMatch)
    if (not goodMatch) and matchCount>1 and matchCount==((len(group)+1)//2)-1:
        pass
        #print('Not quite a match:', name, group)
    return goodMatch #(matchCount>1) or (matchCount >= (len(group)+1)//2)

nameGroupIndex = {}
for name, count in names.most_common():
    if len(name)==1:
        print('single char name', name, count)
    foundGroup = 0
    for gp, group in enumerate(nameGroups):
        dbg = name=='susanna'
        if putInGroup(name, group):
            if dbg:
                print('adding', name, 'to', gp, group)
            if name in nameGroups[gp]:
                print('trying to put', name, 'into', nameGroups[gp])
                sys.exit()
            nameGroups[gp].append(name)
            #nameGroups[gp] = sorted(nameGroups[gp])
            foundGroup = 1
            # if 'ribovics' in nameGroups[gp]:
            #     print(nameGroups[gp])
            break
    if not foundGroup:
        nameGroups.append([name])

print('Number of nameGroups', len(nameGroups))
print('Singleton groups:', sum([1 for ng in nameGroups if len(ng)==1]))

ofile = open('nameMatchesRaw', 'w')
for ngroup in sorted(nameGroups):
    if len(ngroup)>1:
        ofile.write(':'.join(ngroup))
        ofile.write('\n')
ofile.close()
