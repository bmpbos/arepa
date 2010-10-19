REPO_LIST = ['ArrayExpress'] #,\
	     # 'IntAct']


env = Environment() 
SConscript(map(lambda x: x + '/MainSConscript', REPO_LIST)) #, exports=['env'])
