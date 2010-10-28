import SCons
import os
import string 

#//=========================================================================================//
#//=================== General Shell CMD ===================================================//
#//=========================================================================================//

#   SOURCE_0 SOURCE_1 SOURCE_2 .... SOURCE_last > TARGET_0
def _shcmd_Ni_1o_(target,source,env):   # target,source - lists of strings
	print os.getcwd() 
	source_strings = []
	source_strings.append(source[0].get_abspath())
	for i in range (1,len(source)):
		source_strings.append(source[i].rstr())
	os.popen(string.join(source_strings,' ') +\
		  ' > ' + target[0].rstr())


#   SOURCE_0 SOURCE_1 SOURCE_2 .... SOURCE_last-1 < SOURCE_last > TARGET_0
def _shcmd_Nm1i_1i_1o_(target,source,env):   # target,source - lists of strings
	print os.getcwd() 
	source_strings = []
	source_strings.append(source[0].get_abspath())
	for i in range (1,len(source) - 1):
		source_strings.append(source[i].rstr())
	os.popen(string.join(source_strings,' ') + ' < ' + source[len(source) - 1].rstr()  +\
		  ' > ' + target[0].rstr())


#   SOURCE_0 SOURCE_1 SOURCE_2 .... SOURCE_last-2 < SOURCE_last-1 > TARGET_0      - Last input is a FLAG
def _shcmd_Nm1i_1i_1o_iF_(target,source,env):   # target,source - lists of strings
	env.Command(target,source[:-1], _shcmd_Nm1i_1i_1o_)


#def run_pipe_cmds ([cmd1,cmd2,.....]):


#//=========================================================================================//  
#//========================Sleipnir funcs interface=========================================//
#//=========================================================================================//
# TODO: ADD HERE CALL TO ALL SLEIPNIR FUNCTIONS
#def _Dat2Dab_ (target,source,env): 


#def _Normalizer_ (target,source,env): 


#def _Combiner_ (target,source,env): 


#def _KNNImputer_ (target,source,env):
 

def _Distancer_1o_1i_ (target,source,env): 
	os.popen('Distancer -o ' + target[0].rstr() + ' < '+ source[0].rstr())



#def _Combiner_ (target,source,env): 


#def _Combiner_ (target,source,env): 


#//=========================================================================================//
#//========================Download and Uncompress==========================================//
#//=========================================================================================//

# target[1].rstr() - string to download, target[0].rstr() - directory of destination  
def _download_mN_ (target,source,env): 
	print "download_mN in shared funcs", os.getcwd()
	print target[0].rstr()
	print target[1].rstr()

	os.popen('cd ' + target[0].rstr() + ' && wget -N ' + target[1].rstr())


# target[1].rstr() - string to download, target[0].rstr() - directory of destination  
def _download_mmts_ (target,source,env): 
	print "download_mmts in shared funcs", os.getcwd()
	print target[0].rstr()
	print target[1].rstr()

	os.popen('cd ' + target[0].rstr() + ' && wget --timestamping ' + target[1].rstr())


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
