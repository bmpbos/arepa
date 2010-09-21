#!/usr/bin/env ruby

if( ARGV.length != 2 )
	STDERR.puts( "Usage: zip2dirs.rb <data.zip> <data.sdrf>" )
	exit( 0 ); end
strZip, strSDRF = ARGV

hashArrays = {}
aiColumns = []
IO.foreach( strSDRF ) do |strLine|
	astrLine = strLine.chomp.split( /\t/ )
	if( $. == 1 )
		astrLine.each_index do |i|
			if( astrLine[i] =~ /Array Design REF/ )
				aiColumns.push( i ); end; end
	else
		aiColumns.each do |i|
			hashArrays[astrLine[i]] = true; end; end; end

if( strZip !~ /(E-[^-]+-\d+)/ )
	raise( "Illegal file name: " + strZip ); end
strID = $1
`unzip -u #{strZip}`
astrFiles = Dir.glob( strID + "-processed-data-*.txt" )
astrFiles.each do |strFile|
	if( strFile !~ /#{strID}-processed-data-(\d+).txt/ )
		raise( "Illegal extracted file: " + strFile ); end
	strDir = strID + "_" + $1
	`mkdir -p #{strDir}`
	`mv #{strFile} #{strDir}`
	File.open( strDir + "/Makefile", "w" ) do |fileOut|
		fileOut.puts( "IDS_ARRAY	:= " + hashArrays.keys.join( " " ) )
		fileOut.puts( "include ../../Makefile.subdirectory" ); end; end
