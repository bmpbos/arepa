#!/usr/bin/env ruby

if( ARGV.length != 1 )
	raise( "Usage: data2datasets.rb <experiments> < <data>" ); end
strExps = ARGV[0]

hashDescs = {}
IO.foreach( strExps ) do |strLine|
	if( strLine !~ /accession\>([^<]+)\<.*?name\>([^<]+)\</ )
		next; end
	strID, strDesc = $1, $2
	hashDescs[strID] = strDesc; end

STDIN.each do |strLine|
	strLine =~ /^(?:.*\/)?(\S+)\.\S+$/
	strID = strBase = $1
	if( strID =~ /E_([^_]+)_(\d+)(.*)/ )
		strBase = "E-" + $1 + "-" + $2
		strID = strBase + $3; end
	if( strDesc = hashDescs[strBase] )
		strID += ": " + strDesc; end
	puts( strID ); end
