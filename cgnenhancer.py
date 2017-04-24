import sys

#On the use of a single file for multiple classes:
#http://stackoverflow.com/questions/2864366/are-classes-in-python-in-different-files
class Context: 
	#A class for the Context data structure;
	#A Context is a container for related tags
	global GlobTagList
	def __init__(self):
		self.tags=list()
		#tags in the current context should be read from a file
	def addTag(self,myTagName):
		if myTagName in GlobTagList:
			self.tags.append(myTagName)
	def listTags(self):
		return self.tags;
		
class Tag:
	global UrlDatabase
	#Tags refer to external resources (site,articles, etc...) using a unique id number
	def __init__(self):
		self.urls=list()
	def addUrl(self,myUrlName):
		if myUrlName in UrlDatabase : 
			self.append(UrlDatabase[myUrlName])
	def listUrls(self):
		return self.urls;
	
	
def main():
	#Initialize global data structures 
	GlobTagList=list()
	ContextDict=dict()
	#Parse the file with context and tags
	for line in open("contexts.txt"):
		contName, tagNames = line.split(":",1)
		contName.strip('"')
		if contName in ContextDict:
			for tag in tagNames.split('" "'):
				ContextDict[contName].append(tag.strip('"'))
		else:
			ContextDict[contName]=list()
			for tag in tagNames.split('" "'):
				ContextDict[contName].append(tag.strip('"'))
	
	print("End parsing") #DEBUG
	print(ContextDict)   #DEBUG
	sys.exit()				#DEBUG
	
	
	UrlDatabase=dict()
	#TODO: parse the file with urls and update tags  
	
	#This is the main loop 
	exitFlag=False;
	while(not exitFlag):
		print("Cognitive enhancer debug version")
		validChoice=False
		ContextChoice=input("Choose a context number or exit (X): ")
		#TODO: parse ContextChoice variable
		
		if(validChoice):
			if(ContextChoice=="X"): 
				exitFlag=True
		else:
			CurrentContextName=""
			print("Context: "+CurrentContextName)
			#TODO: print the list of available tags
			TagChoice=input("Choose a tag name from the list: ")
			#TODO: parse TagChoice variable
			#TODO: list the urls
			
	return

if __name__=="__main__": main()




