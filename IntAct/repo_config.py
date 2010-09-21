class Repo:
	def __init__(self, repoName, taxoweb,dataweb,):
		self.name = repoName
		self.taxonomy_website = taxoweb
		self.data_website = dataweb #list []


intact = Repo( "IntAct",\
                   "ftp://ftp.ncbi.nih.gov/pub/taxonomy/taxdump.tar.gz",\
                   ["ftp://ftp.ebi.ac.uk/pub/databases/intact/current/psimitab/intact.zip"])
