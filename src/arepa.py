#!/usr/bin/env python

import os
import sfle
import sys
import threading
import glob 
import csv 

#===============================================================================
# ARepA structural metadata
#===============================================================================

def cwd( ):

	return os.path.basename( os.getcwd( ) )

def taxa( strTaxids, fNames = False ):
	
	setRet = set()
	if strTaxids:
		for strLine in open( strTaxids ):
			strID, strName = strLine.strip( ).split( "\t" )
			setRet.add( strName if fNames else strID )
	return setRet

def path_arepa( ):
	
	return sfle.d( os.path.abspath( sfle.d( os.path.dirname( __file__ ), ".." ) ), "" )

def path_repo( ):
	
	strRet = os.getcwd( )
	strRet = strRet[len( path_arepa( ) ):]
	while True:
		strHead, strTail = os.path.split( strRet )
		if not strHead:
			strRet = path_arepa( ) + strRet
			break
		strRet = strHead
	return sfle.d( strRet, "" )

def name_repo( ):
	
	return os.path.basename( os.path.dirname( path_repo( ) ) )

def level( ):

	strPath = path_repo( )
	strPath = os.getcwd( )[len( strPath ):]
	iRet = 0
	while True:
		strHead, strTail = os.path.split( strPath )
		if not strHead:
			break
		iRet += 1
		strPath = strHead
	return iRet

c_strProgSConstruct		= sfle.d( path_arepa( ), sfle.c_strDirSrc, "SConstruct.py" )

#===============================================================================
# R package building 
#===============================================================================
c_strRPackage = "rpackage"

def r_dir( strName = c_strRPackage ):
	strDirMan = sfle.d( strName, "man" )
	strDirData = sfle.d( strName, sfle.c_strDirData )
	if not(os.path.exists(strDirMan)):
		os.makedirs( sfle.d( strName, "man" ) )
	if not(os.path.exists(strDirData)):
		os.makedirs( sfle.d( strName, sfle.c_strDirData ) )
	with open( sfle.d( strName, "NAMESPACE" ), "w" ) as outputf:
		outputf.write( r'exportPattern("^[[:alpha:]]+")' )
	
#===============================================================================
# Gene ID conversion
#===============================================================================

#Constants 
c_strDirMapping		= sfle.d( path_arepa(), "GeneMapper", sfle.c_strDirEtc, "uniprotko" )
c_strFileManualMapping	= sfle.d( path_arepa(), "GeneMapper", sfle.c_strDirEtc, "manual_mapping.txt" )

def genemapper( ):

	return sfle.d( path_arepa( ), sfle.c_strDirSrc, "SConscript_genemapping.py" )

def genemap_genename( ):
	
	return "H"

def genemap_uniref( ):
	
	return "S"

def genemap_probeids( ):
	
	return "X"

s_lockTaxdump	= threading.Lock( )
s_hashTaxID2Org	= None
s_hashOrg2TaxID	= None
def _taxdump( ):
	global	s_lockTaxdump, s_hashTaxID2Org, s_hashOrg2TaxID

	s_lockTaxdump.acquire( )
	if ( s_hashTaxID2Org == None ) or ( s_hashOrg2TaxID == None ):
		s_hashTaxID2Org = {}
		s_hashOrg2TaxID = {}
		strTaxIDs = sfle.d( path_arepa( ), sfle.c_strDirTmp, "taxdump.txt" )
		try:
			for strLine in open( strTaxIDs ):
				strOrg, strID = strLine.strip( ).split( "\t" )
				s_hashTaxID2Org[strID] = strOrg
				s_hashOrg2TaxID[strOrg] = strID
		except IOError:
			pass
	s_lockTaxdump.release( )
	
	return (s_hashTaxID2Org, s_hashOrg2TaxID)

def taxid2org( strTaxID ):

	hashTaxID2Org, hashOrg2TaxID = _taxdump( )
	return hashTaxID2Org.get( strTaxID )

def org2taxid( strOrg, fApprox = False, iLevel = 2 ):
	"""fApprox flag turns on approximate taxid acquisition; 
	includes subspecies. Modified: returns list, not string  
	"""
	hashTaxID2Org, hashOrg2TaxID = _taxdump( )
	if fApprox:
		astrOrgSplit = strOrg.split(" ")
		strOrgApprox = " ".join(astrOrgSplit[:iLevel]) if len(astrOrgSplit)>=2 else strOrg
		astrApproxTaxIDs = filter(lambda s: strOrgApprox in s,hashOrg2TaxID.keys())
		return [hashOrg2TaxID[k] for k in astrApproxTaxIDs] 
	else:
		return hashOrg2TaxID.get( strOrg )

def get_mappingfile( strTaxID, fApprox = True, strDir = c_strDirMapping ):
        if not(strTaxID):
                return None 
        else:
                if not(sfle.isempty(c_strFileManualMapping)):
			pHash = {k:v for k,v in map( lambda a: a.split('\t'),
					sfle.readcomment(open(c_strFileManualMapping)))}
			astrMapOutTmp = filter(bool,[pHash.get(item) for item in 
				[" ".join(taxid2org( strTaxID ).split(" ")[:2])]])
			astrMapOut = map(lambda x: sfle.d( c_strDirMapping, x), astrMapOutTmp) \
				if astrMapOutTmp else []
		if not(astrMapOut):
			# give an un-prioritized list 
                        astrIDs = [strTaxID] if not(fApprox) else org2taxid( taxid2org( strTaxID ), True )
                        for strID in astrIDs:
                                astrGlob =  glob.glob( sfle.d( strDir, strID + "_*" ) )
                                if astrGlob:
                                        astrMapOut = astrGlob
                                        break
                return (astrMapOut[0] if astrMapOut else None)


#------------------------------------------------------------------------------ 

if __name__ == "__main__":
	pass
