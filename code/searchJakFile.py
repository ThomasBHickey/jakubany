#!/usr/bin/python3
import sys
from collections import Counter, defaultdict

def readNameGroups(fname):
    f = open(fname)
    ngs = []
    for line in f.readlines():
        ngs.append(line.strip().lower().split(':'))
    print('read in', len(ngs), 'from', fname)
    return ngs

nameGroups = readNameGroups('nameMatchesRaw')

lines = open(sys.argv[1]).readlines()
#lines = lines[:17]
print('have', len(lines),'lines to search')

def getPos(term, sline):
	#print('looking for', term, 'in', sline)
	for pos, word in enumerate(sline):
		if word==term:
			return pos
	return -1

def getTerms(s):
	terms = []
	for rawterm in s.lower().split():
		t = ''.join([c for c in rawterm if c.isalpha()])
		if len(t):
			terms.append(t)
	return terms

while 1:
	inp = input('Names to search:').lower()
	if inp.lower() in ['quit', 'exit', 'stop', 'q']:
		break
	sterms = inp.split()
	#print('looking for', sterms)
	groupsToUse=[]
	for sterm in sterms:
		groupsToUse.append([sterm])
		for ng in nameGroups:
			if sterm in ng:
				groupsToUse[-1] = ng
				break

	print('using', groupsToUse)
	linePos = 0
	linesFound = 0
	for line in lines:
		linePos += 1
		slowline = getTerms(line)
		#print('slowline:', slowline)
		groupPos = len(groupsToUse)*[-1]
		for gpos, groupToUse in enumerate(groupsToUse):
			for term in groupToUse:
				#print('checking', term)
				if term in slowline:
					#print('found', term)
					groupPos[gpos] = getPos(term, slowline)
					#print('pos:', groupPos[gpos])
					break
		#print('groupPos:', groupPos)
		if min(groupPos)!=-1:
			print('>>', line.rstrip())
			linesFound += 1
	print('Found', linesFound,'lines')

