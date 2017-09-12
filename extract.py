import sys
from cgnenhancer import Context, Tag
def extract(namefile):
	UrlDatabase = dict()
	url_list = open(namefile, 'r')
	global GlobTagList
	GlobTagList = list()
	#builds a dictionary with urls as keys and urls as values
	for line in url_list:
		junk_line, line = line.split("=", 1)
		url, line = line.split(" ", 1)
		url = url.strip('"')
		junk_line, line = line.split("tags=") 
		tags, junk_line = line.split(">", 1)
		tags = tags.strip('"')
		tag_list = tags.split(",")
		UrlDatabase[url] = tag_list
		
	for key in UrlDatabase:	#DEBUG
		print key, UrlDatabase[key]
		
	TagDatabase = dict()
	
	for key in UrlDatabase:
		for tag in UrlDatabase[key]:
			TagDatabase[tag] = list()
	for key in UrlDatabase:
		for tag in UrlDatabase[key]:
			TagDatabase[tag].append(key)

	#creates list of Tag objects
	GlobTagList = [Tag(TagDatabase.keys()[i]) for i in range(len(TagDatabase))]
	for item in GlobTagList:
		print item.name #DEBUG
	for key in TagDatabase
		
	url_list.close()
	
extract('urls.html')
