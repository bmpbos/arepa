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

import arepa
import os
import sfle
import sys

c_afileSConscripts	= sorted( Glob( sfle.d( arepa.path_repo( ), sfle.c_strDirSrc, "SConscript*" ) ) )

if os.path.isfile( "SConscript" ):
	exec(compile(open( "SConscript" ).read(), "SConscript", 'exec'))
else:
	hashArgs = {}

# I tried very hard to do this using import, but I can't find a way to prematurely
# halt an import without sys.exit, which kills the entire process.
for fileSConscript in c_afileSConscripts:
	strSConscript = fileSConscript.get_abspath( )
	hashEnv = {"test" : lambda *a: False, "testing" : True}
	try:
		exec(compile(open( strSConscript ).read(), strSConscript, 'exec'), hashEnv)
	except SystemExit:
		pass
	if hashEnv["test"]( arepa.level( ), arepa.cwd( ), hashArgs ):
		exec(compile(open( strSConscript ).read(), strSConscript, 'exec'))
