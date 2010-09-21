#!/usr/bin/env ruby

if( ARGV.length != 1 )
	raise( "Usage: pcl2ko.rb <koc> < <data.pcl>" ); end
strKOC = ARGV[0]

hashKOs = {}
IO.foreach( strKOC ) do |strLine|
	astrLine = strLine.strip.split( /\t/ )
	astrLine[1, astrLine.length].each do |strToken|
		strOrg, strGene = strToken.split( /\#/ )
		if( !( astrKOs = hashKOs[strGene] ) )
			hashKOs[strGene] = astrKOs = []; end
		astrKOs.push( astrLine[0] ); end; end

fHit = false
STDIN.each do |strLine|
	if( strLine !~ /^([^\t]+)(.+)/ )
		next; end
	strGene, strRest = $1, $2
	if( ( $. == 1 ) || ( strGene == "EWEIGHT" ) )
		puts( strLine )
		next; end
	( hashKOs[strGene] || [] ).each do |strKO|
		fHit = true
		puts( strKO + strRest ); end; end
if( !fHit )
	puts( "NULL	NULL	1	" ); end
