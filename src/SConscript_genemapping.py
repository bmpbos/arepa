#!/usr/bin/env python
'''
Shared utility for magic functions within
gene mapper 
'''

import arepa
import os
import sys 
import sfle 
import pickle 
import itertools 
import re 
import glob 

g_iterCounter			= itertools.count(0) 

c_strID 			= arepa.cwd( )
c_strPathRepo			= arepa.name_repo( )
c_strSufMap 			= ".map" 
c_strMapped			= "_mapped" 
c_strDirData			= sfle.d( arepa.path_repo( ), sfle.c_strDirData )
c_strDirManMap			= sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_mapping" )
c_astrGeneTo			= sfle.readcomment( sfle.d( arepa.path_arepa(),sfle.c_strDirEtc,"geneid" ) 
					or [arepa.genemap_genename( )] ) 
c_strPathGeneMapper		= sfle.d( arepa.path_arepa(), "GeneMapper" )
c_strPathTopMapping		= sfle.d( c_strPathGeneMapper, sfle.c_strDirEtc, "manual_mapping" )
c_strPathUniprotKO		= sfle.d( c_strPathGeneMapper, sfle.c_strDirEtc, "uniprotko" )
c_fileProgMakeUnique		= sfle.d( arepa.path_arepa(), sfle.c_strDirSrc,"makeunique.py")
c_funcGeneMapper		= sfle.d( c_strPathGeneMapper, sfle.c_strDirSrc, "bridgemapper.py" )

c_pHashBridgeDB 		= dict((strName, sfle.d( arepa.path_arepa( ), "GeneMapper", sfle.c_strDirEtc, strDB )) 
	for strName, strDB in (
	("Homo sapiens",		"Hs_Derby_20120602.bridge"),
	("Mus musculus",		"Mm_Derby_20120602.bridge"),
	("Saccharomyces cerevisiae",	"Sc_Derby_20120602.bridge"),
		))

pHashBridgeDBTaxIDs = {k:arepa.org2taxid( k, True ) for k in c_pHashBridgeDB.keys()}

def funcCounter( iter ):
	return ( "%02d" % next( iter ) )

def funcGeneIDMapping( pE, fileDATin, strGeneFrom, strLOGout, strMAPin = None, aiCOL = [0,1], iSkip = 0 ):
	try:
		int(strMAPin)
		strTaxa, strMAPin = strMAPin, None
	except (ValueError, TypeError):
		strTaxa = None
	if not(strMAPin):
		strDirAuto = c_strDirData if ( c_strID == c_strPathRepo ) else "" 
		strAutoMAPtmp = sfle.d( strDirAuto, c_strID + c_strSufMap )
		strAutoMAP = strAutoMAPtmp if os.path.exists( strAutoMAPtmp ) else None 
		# Use manual mapping files, files that are deeper down have priority
		#else try automatically generated mapping file
		strTopMAP = reduce( lambda x,y: x or y, glob.glob( sfle.d( c_strPathTopMapping, 
			"*" + c_strSufMap ) ), None )
		strMAPManTmp = sfle.d( c_strDirManMap, c_strID + c_strSufMap )
		strMAPin = (strMAPManTmp if os.path.exists( strMAPManTmp) else None) or strTopMAP or strAutoMAP  
		sys.stderr.write( strMAPin + '\n' )
		# Else find taxid 
		if not(strMAPin) and not(strTaxa):
			astrMatch = re.findall( r'taxid_([0-9]+)', c_strID )
			strTaxa = astrMatch[0].strip( ) if astrMatch else None
		# Use provided mapping files  
		if not(strMAPin) and strTaxa:
			for strMAPname in glob.glob(sfle.d( c_strPathUniprotKO, "*.map" )):
				if re.search( r'\D' + strTaxa + r'\D', strMAPname ):
					strMAPin = strMAPname
					break
		# Else ask arepa to figure out an appropriate mapping file 
		if not(strMAPin) and strTaxa:
			strMAPin = arepa.get_mappingfile( strTaxa )
		# Else use BridgeDB files
		if not(strMAPin) and strTaxa:
			for strSpeciesName in c_pHashBridgeDB.keys():
				if strSpeciesName in arepa.taxid2org( strTaxa ):
					strMAPin = c_pHashBridgeDB[strSpeciesName]
					break 
		
	strBase, strExt = os.path.splitext( str(fileDATin) )
	strCount = funcCounter( g_iterCounter )
	strT = strBase + c_strMapped + strCount + strExt
	afileRet = sfle.op( pE, c_funcGeneMapper, [[fileDATin], [True, strT],
		"-c", str(aiCOL), "-f", strGeneFrom, "-t", c_astrGeneTo[0],
		"-s", iSkip, "-l", [True, strLOGout]] +
		( ["-m", [strMAPin]] if strMAPin else [] ) )
	pE.Depends( afileRet, sfle.scons_child( pE, c_strPathGeneMapper ) )
	return afileRet

def funcMakeUnique( pE, fileDATin, iSkip = 0, iCol = 2 ):
	strBase, strExt = os.path.splitext(str(fileDATin))
	iCount = funcCounter( g_iterCounter )
	strT = re.sub( r'_mapped[0-9]+', c_strMapped + iCount, str(fileDATin))
	return sfle.op(pE, c_fileProgMakeUnique, [[fileDATin], [True,strT],"-s", iSkip, "-c", iCol])
