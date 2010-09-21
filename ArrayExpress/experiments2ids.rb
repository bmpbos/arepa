#!/usr/bin/env ruby

if( ARGV.length != 1 )
	raise( "Usage: experiments2ids.rb <species.txt> < <experiments>" ); end
strSpecies = ARGV[ 0 ]

hashSpecies = {}
IO.foreach( strSpecies ) do |strLine|
	hashSpecies[ strLine.strip ] = true; end

hashIDs = {}
STDIN.each do |strLine|
	if( strLine !~ /accession\>([^<]+)\<.*species\>([^<]+)\</ )
		next; end
	strID, strSpecies = $1, $2
	if( hashSpecies[ $2 ] )
		hashIDs[ $1 ] = true; end; end

puts( hashIDs.keys.join( "\n" ) )
