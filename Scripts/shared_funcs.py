import SCons
import os
import string 

#//=========================================================================================//
#//=================== General Shell CMD ===================================================//
#//=========================================================================================//

#   SOURCE_0 SOURCE_1 SOURCE_2 .... SOURCE_last > TARGET_0
def _runshcmd1_(target,source,env):   # target,source - lists of strings
	print os.getcwd() 
	source_strings = []
	source_strings.append(source[0].get_abspath())
	for i in range (1,len(source)):
		source_strings.append(source[i].rstr())
	os.popen(string.join(source_strings,' ') +\
		  ' > ' + target[0].rstr())


#   SOURCE_0 SOURCE_1 SOURCE_2 .... SOURCE_last-1 < SOURCE_last > TARGET_0
def _runshcmd2_(target,source,env):   # target,source - lists of strings
	print os.getcwd() 
	source_strings = []
	source_strings.append(source[0].get_abspath())
	for i in range (1,len(source) - 1):
		source_strings.append(source[i].rstr())
	os.popen(string.join(source_strings,' ') + ' < ' + source[len(source) - 1].rstr()  +\
		  ' > ' + target[0].rstr())

#def run_pipe_cmds ([cmd1,cmd2,.....]):


#//=========================================================================================//  
#//========================Sleipnir funcs interface=========================================//
#//=========================================================================================//
# TODO: ADD HERE CALL TO ALL SLEIPNIR FUNCTIONS
#def _Dat2Dab_ (target,source,env): 


#def _Normalizer_ (target,source,env): 


#def _Combiner_ (target,source,env): 


#def _KNNImputer_ (target,source,env):
 

#def _Distancer_ (target,source,env): 


#def _Combiner_ (target,source,env): 


#def _Combiner_ (target,source,env): 


#//=========================================================================================//
#//========================Download and Uncompress==========================================//
#//=========================================================================================//


#def _download_ (target,source,env): 

def _untar_ (target,source,env): 
	print 'UNTAR in shared funcs', os.getcwd()
	repodir = string.join(string.split(source[0].rstr(),'/')[:-1],'/')
	os.popen('tar --directory=' + repodir + ' -xzf ' + source[0].rstr())


#def _unzip_ (target,source,env): 


#//=========================================================================================//
#//===========================Metadata======================================================//
#//=========================================================================================//	

#def _metadata_search_ (target,source,env): 

#def _metadata_update_ (target,source,env): 

#//=========================================================================================//
#//===========================Gene identifier===============================================//
#//=========================================================================================//	

#def _get_kegg_id_ (target,source,env):

#def _update_kegg_id_table_ (target,source,env):      #hash table {some gene id : kegg id}

#//=========================================================================================//
#//===========================Species=======================================================//
#//=========================================================================================//	

#def _get_species_description_ (target,source,env):   #hash table {species id : description} 

#//=========================================================================================//
#//===========================Species=======================================================//
#//=========================================================================================//	




