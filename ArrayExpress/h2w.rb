#!/usr/bin/env ruby

if( ARGV.length != 1 )
	raise( "Usage: h2w.rb <hubs.txt>" ); end
strHubs = ARGV[0]

strHubs =~ /^(?:.*\/)?(\S+)(?:_h)?\./
strBase = $1

puts( "GID	NAME	GWEIGHT	" + strBase )
puts( "EWEIGHT			1" )
fHit = false
IO.foreach( strHubs ) do |strLine|
	if( ( $. == 1 ) || ( strLine =~ /^total/ ) )
		next; end
	strPath, strGenes, strHub, strHubStd, strHubN, strCliq, strCliqStd,
		strCliqN = strLine.strip.split( /\t/ )
	fOk = [strHub, strHubStd, strCliq, strCliqStd].inject( true ) do |fCur, str|
		fCur && !%w(inf nan).include?( str.downcase ); end
	if( !fOk || ( strGenes.to_i < 3 ) )
		next; end
	dHub, dHubStd, dCliq, dCliqStd = [strHub, strHubStd, strCliq,
		strCliqStd].map do |str|
		str.to_f; end
	fHit = true
	puts( [strPath, strPath, 1, ( dCliq - dHub ) * 2 /
		( dHubStd + dCliqStd )].join( "\t" ) ); end
if( !fHit )
	puts( "NULL	NULL	1	" ); end
