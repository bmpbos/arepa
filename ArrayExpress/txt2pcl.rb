#!/usr/bin/env ruby

# Haemophilus influenzae symbols -> IDs
#C_astrMaps	= Dir.glob( "../../maps/*.txt" )
C_astrMaps	= Dir.glob( "maps/*.txt" )

C_astrPres	= %w(Cj Ng Sa Ye Cd Rv Hi Mb Bb CBO Cg Ef FTT FTL HP Nm Pa Vc VCA Ecs Ba BSU RL lmo SCO Xf)

def make_label( hashMetadata, hashhashMap, strToken )

	strOR = C_astrPres.map do |str|
		"(?:" + str + ")"; end.join( "|" )
	if( strToken =~ /^(.*)\s+\([0-9A-Z]+\)$/ )
		strToken = $1; end
	if( strToken =~ /:([^:]+_at)/ )
		strToken = $1; end

	hashTokens = {strToken => true}
	iSize = -1
	while( hashTokens.size != iSize )
		iSize = hashTokens.size
		hashTokens.keys.each do |strCur|
			( hashhashMap[strCur] || {} ).keys.each do |strKey|
				hashTokens[strKey] = true; end; end; end

#	[strToken].concat( ( hashhashMap[strToken] || {} ).keys ).each do |strCur|
	hashTokens.keys.each do |strCur|
		strCur = strCur.strip
		strRet = nil
		case( strCur )
			when /(oe\d+[fr](?:-\d+)?)/i
				strRet = $1.upcase

			when /(EF)_(\d+).*at/
				strRet = $1 + $2

			when /(SG)(\d+).*at/i
				strRet = $1 + "O_" + $2

			when /((?:ba)|(?:ftt)|(?:nma))(\d+)/i
				strRet = $1 + "_" + $2

			when /(sp[rn]?_\d+)/i
				strRet = $1

			when /(sp[rn]?)(\d+)(?:#\d+)?$/i
				strRet = $1 + "_" + $2

			when /HPY(\d+)/
				strRet = "HP" + $1

			when /(#{strOR})\S*-(\d+)/
				strRet = ( $1 + $2 ).upcase

			when /((?:#{strOR})\d+)/i
				strRet = $1.upcase

			when /(b\d+)/i
				strRet = $1.upcase; end
		if( strRet )
			return strRet; end; end

	return strToken; end

if( ARGV.length == 0 )
	raise( "Usage: txt2pcl.rb <metadata.txt> <array.adf>* < <data.txt>" ); end
strMetadata = ARGV[0]
astrADFs = ARGV[1, ARGV.length].concat( C_astrMaps )

hashMetadata = {}
IO.foreach( strMetadata ) do |strLine|
	strKey, strValue = strLine.strip.split( /\t/ )
	hashMetadata[strKey] = strValue; end

hashhashMap = {}
astrADFs.each do |strADF|
	aiCols = ( strADF =~ /adf.txt/ ) ? [4, 5] : [0, 1]
	IO.foreach( strADF ) do |strLine|
		astrLine = strLine.chomp.split( /\t/ )
		strFrom, strTo = astrLine[aiCols[0]], astrLine[aiCols[1]]
		if( !( strFrom && strTo ) )
			next; end
		if( !( hashTos = hashhashMap[strFrom] ) )
			hashhashMap[strFrom] = hashhashMap[strFrom.upcase] = hashTos = {}; end
		hashTos[strTo] = true; end; end

strMetadata =~ /E-([^-]+)-\d+/
strType = $1

aiColumns = astrLabels = nil
hashLog = {}
hashLabel = {}
hashBackgrounds = {}
fGenes = false
STDIN.each do |strLine|
	astrLine = strLine.strip.split( /\t/ )
	if( $. == 1 )
		astrLabels = astrLine
		next; end
	if( aiColumns )
		astrOut = aiColumns.map do |iColumn|
			strTok = astrLine[iColumn]
			if( hashLabel[iColumn] )
				make_label( hashMetadata, hashhashMap, strTok )
			elsif( iBG = hashBackgrounds[iColumn] )
				if( ( strTok.length == 0 ) || ( strTok =~ /NULL/i ) ||
					!( strBG = astrLine[iBG] ) || ( strBG.length == 0 ) ||
					( strBG =~ /NULL/i ) )
					""
				else
					if( ( d = astrLine[iColumn].to_f - strBG.to_f ) > 0 )
						sprintf( "%g", Math.log( d ) / Math.log( 2 ) )
					else
						""; end; end
			elsif( !hashLog[iColumn] )
				( strTok =~ /NULL/i ) ? "" : strTok
			else
				if( !strTok || ( strTok.length == 0 ) || ( strTok =~ /NULL/i ) )
					""
				elsif( ( d = astrLine[iColumn].to_f ) > 0 )
					sprintf( "%g", Math.log( d ) / Math.log( 2 ) )
				else
					""; end; end; end
		astrOut.insert( 1, astrOut[0] )
		astrOut.insert( 2, 1 )
		fGenes = true
		puts( astrOut.join( "\t" ) )
	else
		iPrev = nil
		aiColumns = []
		astrHeaders = []
		fID = false
		astrLine.each_index do |i|
			case( astrLine[i] )
				when /(?:Systematic)|(?::Gene)|(?:Gene ID)|(?:NAME\/ID)/
					if( aiColumns.length == 0 )
						fID = true
						aiColumns.push( i )
						astrHeaders.push( "ID" )
						hashLabel[i] = true; end

				when /(?:Software Unknown:log ratios)|(?:LOG2RATIO CH1\/CH2)|(?:SMD:RESULT.LOG_RAT2N_MEAN)|(?:glog ratio)|(?:Software Unknown:Log\(base2\) of R\/G Normalized Ratio \(Mean\))|(?:Software Unknown:RatNormMAD)|(?:Software Unknown:Ratio)|(?:SMD:LOG_RAT2N_MEDIAN)|(?:GenePix:Log Ratio \(635\/532\))|(?:Software Unknown:log2 ratio test vs reference)|(?:Software Unknown:M)|(?:Feature Extraction Software:LogRatio)|(?:Feature Extraction Software:norm_Log10Ratio)|(?:Software Unknown:Normalized \(mutant\/wild type\))/
					aiColumns.push( i )
					astrHeaders.push( astrLabels[i] )

				when /(?:Software Unknown:)?Signal Median/
					aiColumns.push( i )
					astrHeaders.push( astrLabels[i] )
					iPrev = i

				when /(?:Software Unknown:)?Background Median/
					hashBackgrounds[iPrev] = i

				when /^(?:ratio)|(?:Software Unknown:Normalised)$/
					case( strType )
						when "BUGS"
							aiColumns.push( i )
							astrHeaders.push( astrLabels[i] ); end

				when /(?:GEO:AFFYMETRIX_VALUE)|(?:Affymetrix:CHPSignal)/
					case( strType )
						when "GEOD", "MEXP"
							aiColumns.push( i )
							astrHeaders.push( astrLabels[i] )
							hashLog[i] = true; end

				when /(?:Software Unknown:)?Normalized/
					case( strType )
						when "BUGS"
							aiColumns.push( i )
							astrHeaders.push( astrLabels[i] )
							hashLog[i] = true; end; end; end
		if( !fID )
			hashLabel[0] = true
			aiColumns.insert( 0, 0 )
			astrHeaders.insert( 0, astrLine[0] ); end
		astrHeaders.insert( 1, "NAME" )
		astrHeaders.insert( 2, "GWEIGHT" )
		if( astrHeaders.length < 4 )
			astrHeaders.push( "NULL" ); end
		puts( astrHeaders.join( "\t" ) )
		puts( "EWEIGHT		" + ( "	1" * ( astrHeaders.length -
			3 ) ) ); end; end

if( !fGenes )
	puts( "NULL	NULL	1" + ( "\t" * ( astrHeaders.length - 3 ) ) ); end
