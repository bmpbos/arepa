#!/usr/bin/env ruby

C_iSkip			= 2
C_iLines		= 100
C_hashColumns	= {
	"Characteristics [Organism]"	=> "Species"
}

if( ARGV.length < 2 )
	raise( "Usage: metadata.rb <data.pcl> <metadata.sdrf> <array.adf>+" ); end
strPCL, strSDRF = ARGV[0, 2]
astrADFs = ARGV[2, ARGV.length]

astrHeaders = nil
aiColumns = []
hashValues = {}
IO.foreach( strSDRF ) do |strLine|
	astrLine = strLine.chomp.split( /\t/ )
	if( astrHeaders )
		aiColumns.each do |iColumn|
			if( ( strValue = astrLine[iColumn] ) && ( strValue.length > 0 ) )
				hashValues[C_hashColumns[astrHeaders[iColumn]]] =
					strValue; end; end
	else
		astrHeaders = astrLine
		astrHeaders.each_index do |iColumn|
			if( C_hashColumns[astrHeaders[iColumn]] )
				aiColumns.push( iColumn ); end; end; end; end

hashValues["Assayed"] = "transcript expression"
hashValues["Assay"] = "microarray"
if( strPCL != "0" )
	iNegative = 0
	IO.foreach( strPCL ) do |strLine|
		if( $. > C_iLines )
			break; end
		astrLine = strLine.chomp.split( /\t/ )
		if( $. == 1 )
			hashValues["Conditions"] = astrLine.length - C_iSkip - 1
		else
			(( C_iSkip + 1 )...astrLine.length).each do |i|
				if( astrLine[i] && ( astrLine[i].length > 0 ) &&
					( ( d = astrLine[i].to_f ) < -0.5 ) )
					iNegative += 1; end; end; end; end
	hashValues["Channels"] = ( iNegative > 3 ) ? 2 : 1; end

hashValues.each do |strKey, strValue|
	if( ( strKey =~ /^Species$/ ) && ( strValue =~ /^(\S+\s+\S+)/ ) )
		strValue = $1; end
	puts( [strKey, strValue].join( "\t" ) ); end
