#!/usr/bin/env python

import arepa
import cfile
import re
import sys

c_iColumns	= 16


def callback( aArgs, strInterID, strAltAs , strAltBs , strSynAs , strSynBs , strSynAs2, strSynBs2, strAs, strBs, strSynAs3, strSynBs3, strMethods, strTypes, strAuthors, strPMIDs, strTaxAs):
	setPairs, strTaxID, hashCache = aArgs
	astrAB = []
	for astrCur in ([strAs, strAltAs, strSynAs], [strBs, strAltBs, strSynBs]):
		astrTokens = []
		for strTokens in astrCur:
			astrTokens += strTokens.split( "|" )
		strGene = None
		for strToken in astrTokens:
			strType, strID, strGloss = cfile.split( strToken )
			strCur = hashCache.get( strID )
			if strCur == None:
				strCur = hashCache[strID] = strID 
			if strCur:
				strGene = strCur
				break
		astrAB.append( strGene or astrTokens[0] )
	setPairs.add( tuple(sorted( astrAB )) )

if len( sys.argv ) != 2:
	raise Exception( "Usage: c2txt.py <id> < <biogridc.txt>" )
strTarget = sys.argv[1]

mtch = re.search( 'taxid_(\d+)', strTarget )
if not mtch:
	raise Exception( "Illegal target: " + strTarget )
strTaxID = mtch.group( 1 )

setPairs = set()
cfile.read( sys.stdin, c_iColumns, strTarget, callback, [setPairs, strTaxID, {}] )
for astrGenes in setPairs:
	print( "\t".join( list(astrGenes) + ["1"] ) )


