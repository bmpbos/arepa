#!/usr/bin/env ruby

STDIN.each do |strID|
	if( strID !~ /E-([^-]+)-\d/ )
		STDERR.puts( "WARN - illegal ID: " + strID )
		next; end
	strID.strip!
	system( "mkdir -p " + strID )
	strTo = strID + "/Makefile"
	if( !File.exist?( strTo ) )
		system( "cp Makefile.template " + strTo ); end; end
	#strTo2 = strID + "/SConscript"
	#if( !File.exist?( strTo2 ) )
	#	system( "cp SConscript.common " + strTo2);  end; end

