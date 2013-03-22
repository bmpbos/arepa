#!/usr/bin/env python 
'''
Microarray pipeline -- gene mapping, normalization, imputation, 
co-expression network construction
'''
import sys
import csv
import pickle
import sfle
import arepa
import os
import metadata
import glob 
from subprocess import call as ex 

c_aiCOL            = [0]
c_iSkip            = 2
c_iCOL             = len(c_aiCOL)
c_fileIDNormPCL    = sfle.d( pE, c_strID + "_01norm.pcl" )
c_fileIDPCL        = sfle.d( pE, c_strID + ".pcl" )
c_fileIDDAB        = sfle.d( pE, c_strID + ".dab" )
c_fileIDQUANT      = sfle.d( pE, c_strID + ".quant" )
c_fileIDPKL        = sfle.d( pE, c_strID + ".pkl" )
c_fileStatus       = sfle.d( pE, "status.txt" )
c_fileIDMap        = sfle.d( pE, c_strID + ".map" )
c_fileIDMapRaw     = sfle.d( pE, c_strID + "_raw.map" )
c_strDirManMap     = sfle.d( arepa.path_repo( ), sfle.c_strDirEtc, "manual_mapping" )

c_fileIDMappedPCL  = sfle.d( pE, c_strID + "_00mapped.pcl" )
c_fileIDMappedPCL2 = sfle.d( pE, c_strID + "_01mapped.pcl" )

c_fileFlagSleipnir = sfle.d( pE, arepa.path_repo( ), sfle.c_strDirEtc, "sleipnir" )

#Load GeneMapper SConscript 
execfile( arepa.genemapper( ) )

#- Normalize
def funcIDNormPCL( target, source, env, iMaxLines = 100000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[1] if ( len(sfle.readcomment(astrSs[1])) > c_iSkip ) else astrSs[0] 
	iLC = sfle.lc( strS )
	return ( sfle.ex( "Normalizer -t pcl -T medmult < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )

#- Impute
def funcIDKNNPCL( target, source, env, iMaxLines = 40000 ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( "KNNImputer < " + strS, strT )
		if ( iLC < iMaxLines ) else sfle.ex( "head -n 3 < " + strS, strT ) )

#- PCL -> DAB
def funcIDDAB( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return ( sfle.ex( (sfle.cat( strS ), " | Distancer -o", strT) )
		if ( iLC > 3 ) else sfle.ex( "echo", strT ) )

#- Generate Quant files
def funcIDQUANT( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strS = astrSs[0]
	iLC = sfle.lc( strS )
	return (sfle.ex("echo '-1.5\t-0.5\t0.5\t1.5\t2.5\t3.5\t4.5' >" + strT))

def funcRawMap( target, source, env ):
	strT, astrSs = sfle.ts( target, source )
	strGPLTXTGZ, strRMeta, strProgAnnot2Map, strProgGPL2TXT = astrSs[:4]
	pid = [row for row in csv.DictReader(open( strRMeta ))][0]["platform_id"] 
	strGPLID = c_strID.split("-")[1] if len( c_strID.split("-") ) == 2 else pid
	if not(sfle.isempty(str(strGPLTXTGZ))):
		ex( [strProgAnnot2Map, strGPLTXTGZ, strT] )
	else:
		ex( [strProgGPL2TXT, c_strGPLPath + strGPLID, strT] )

def funcMergeMap( target, source, env ):
	strT, astrSs = sfle.ts( target, source)
	fileTaxa, fileMerge, fileIDRaw =  astrSs[:3]
	astrTaxa = sfle.readcomment(fileTaxa)
	strMap = arepa.get_mappingfile( astrTaxa[0] ) if astrTaxa else ""
	return ( sfle.ex( [fileMerge, fileIDRaw, strMap, strT] ) if strMap else sfle.ex(["cp", fileIDRaw, strT]) )

def funcPCL2DAB( pE, fileIDRawPCL, fileGPLTXTGZ, fileProgAnnot2Map, fileProgMergeMapping, fileTaxa ):
	
	astrSleipnir = sfle.readcomment(c_fileFlagSleipnir)
	bSleipnir = astrSleipnir[0]=="True" if astrSleipnir else False   

	print "sleipnir", ("On" if bSleipnir else "Off")
	#Produce raw mapping file for gene mapping 
	astrMapRaw = pE.Command( c_fileIDMapRaw, [fileGPLTXTGZ, c_fileRMetadataTXT, fileProgAnnot2Map, c_fileProgGPL2TXT], funcRawMap )
	
	#Produce merged mapping file
	astrMap = pE.Command( c_fileIDMap, [fileTaxa, fileProgMergeMapping, astrMapRaw[0]], funcMergeMap )
	
	#Perform Gene Mapping 
	astrMapped = funcGeneIDMapping( pE, fileIDRawPCL, arepa.genemap_probeids( ),
		c_fileStatus, astrMap[0], c_aiCOL, c_iSkip )

	#Get rid of duplicate identifiers 
	astrUnique = funcMakeUnique( pE, astrMapped[0], c_iSkip, c_iCOL ) 

	if bSleipnir:  
		pE.Command( c_fileIDNormPCL, [c_fileIDRawPCL, astrUnique[0]], funcIDNormPCL )
		pE.Command( c_fileIDPCL, c_fileIDNormPCL, funcIDKNNPCL )
		pE.Command( c_fileIDDAB, c_fileIDPCL, funcIDDAB )
		pE.Command( c_fileIDQUANT, c_fileIDPCL, funcIDQUANT )
	else:
		sfle.sop( pE, "cp", [[astrUnique[0]], [True, c_fileIDPCL]] )	
