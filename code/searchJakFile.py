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

nameGroups = readNameGroups('nameMatches')

lines = open(sys.argv[1]).readlines()
#lines = lines[:17]
inMarriageFile = 'Marriages' in sys.argv[1]
inBaptismFile = 'Baptisms' in sys.argv[1]
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
		t = ''
		for c in rawterm:
			if c.isalpha():
				t += c
		if len(t):
			terms.append(t)
	# print('rows[7]:"%s"'%rows[7])
	rows = s.split('\t')
	if inMarriageFile:
		for rn in [6,7]:
			if rows[rn].strip().isdigit():
				terms.append('house:%s'%rows[rn].strip())
	if inBaptismFile:
		if rows[8].strip().isdigit():
			terms.append('house:%s'%rows[8].strip())
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

	print('using', groupsToUse, file=sys.stderr)
	linePos = 0
	linesFound = 0
	for line in lines:
		linePos += 1
		# if linePos==1731:
		# 	splitLine = line.split('\t')
		# 	for r in range(len(splitLine)):
		# 		print(r, splitLine[r].strip())
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
			print(linePos, '>>', line.rstrip())
			linesFound += 1
	break
	print('Found', linesFound,'lines', file=sys.stderr)

