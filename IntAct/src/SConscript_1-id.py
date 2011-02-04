#!/usr/bin/env python

import arepa
import os
import sys

def test( iLevel, strID, hashArgs ):
	return ( iLevel == 1 )
if locals( ).has_key( "testing" ):
	sys.exit( )

#Import( "pE" )
c_strID				= arepa.cwd( )
c_strInputIntactC	= arepa.d( arepa.path_repo( ), arepa.c_strDirTmp, "intactc" )
c_strFileIDTXT		= c_strID + ".txt"
c_strFileIDDAB		= c_strID + ".dab"
c_strProgC2Metadata	= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "c2metadata.py" )
c_strProgC2DAT		= arepa.d( arepa.path_repo( ), arepa.c_strDirSrc, "c2dat.py" )

afileIDTXT = arepa.pipe( pE, c_strInputIntactC, c_strProgC2Metadata, c_strFileIDTXT,
	[[False, c_strID]] )
Default( afileIDTXT )

def funcDAB( target, source, env ):
	strT, astrSs = arepa.ts( target, source )
	strProg, strIn = astrSs
	return arepa.ex( " ".join( [strProg, c_strID, "<", strIn, "| Dat2Dab -o", strT] ) )
afileIDDAB = Command( c_strFileIDDAB, [c_strProgC2DAT, c_strInputIntactC], funcDAB )
Default( afileIDDAB )
