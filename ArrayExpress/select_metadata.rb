#!/usr/bin/env ruby

if( ARGV.length < 2 )
	raise( "Usage: select_metadata.rb <key> <value> [ext=dab]" ); end
strKey, strValue, strExt = ARGV
strExt ||= ".dab"

#astrMetadata = Dir.glob( "E-*/*/*_*.txt" )
astrMetadata = Dir.glob( File.dirname( $0 ) + "/E-*/*/*_*.txt" )
astrMetadata.each do |strFile|
	if( strFile !~ /^(.*\/)?(\S+)\.txt$/ )
		raise( "Illegal metadata file: " + strFile ); end
	strDAB = $1 + $2 + strExt

	fHit = false
	IO.foreach( strFile ) do |strLine|
		astrLine = strLine.strip.split( /\t/ )
		if( ( astrLine[0] == strKey ) && ( astrLine[1] == strValue ) )
			fHit = true
			break; end; end
	if( fHit )
		puts( strDAB ); end; end
