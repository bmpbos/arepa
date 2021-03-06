#!/usr/bin/env python
"""
ARepA: Automated Repository Acquisition 

ARepA is licensed under the MIT license.

Copyright (C) 2013 Yo Sup Moon, Daniela Boernigen, Levi Waldron, Eric Franzosa, Xochitl Morgan, and Curtis Huttenhower

Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation 
files (the "Software"), to deal in the Software without restriction, including without limitation the rights to 
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons 
to whom the Software is furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all copies or 
substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, 
INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. 
IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, 
WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE 
OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
"""

import csv
import os 
import sys
import sfle

def funcGetGSMids( ):
	aRet = [] 
	for astrLine in csv.reader( sys.stdin, csv.excel_tab ):
		if not ( astrLine and astrLine[0] and ( astrLine[0][0] == "!" ) ):
			continue
		strFrom = astrLine[0][1:]
		if "Sample_supplementary_file" in strFrom:
			aRet += [os.path.basename(x) if \
				"CEL" in os.path.basename(x) else "#" + \
				os.path.basename(x) for x in astrLine[1:]]
	return aRet 

#Execute
sys.stdout.write( "\n".join( funcGetGSMids( ) ) ) 
