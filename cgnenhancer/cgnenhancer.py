import sys, os, urllib

class Context: 
    #A class for the Context data structure;
    #A Context is a container for related tags
    def __init__(self,GlobTagList):
        self.tags=list()
        #tags in the current context should be read from a file
    def addTag(self,myTagName):
        if myTagName in GlobTagList:
            self.tags.append(myTagName)
        else:
            GlobTagList.append(myTagName)
            self.tags.append(myTagName)
    def listTags(self):
        return self.tags;
    def listArticles(self):
        contextArticleList=list()
        for tag in tags:
            for article in tag.listArticles():
                if article not in contextArticleList:
                    contextArticleList.append(article)
        return contextArticleList
            
class Tag:
    #Tags refer to external resources (site,articles, etc...) using a unique id number
    def __init__(self):
        self.articles=list()
    def addArticle(self,myUrlName):
        newArticle=Article(myUrlName)
        if newArticle in self.articles: 
            self.articles.append(newArticle)
    def listArticles(self):
        return self.articles
    
    
class Article:
    self.url=""
    self.title=""
    self.preview=""
    
    def __init__(self, MyUrl):
        #parse html page / local database (?) 
        return
    def GetTitle(self):
        return self.title
    def GetPreview(self):
        return self.title
    
    
def init():
    #Global data structures
    TagList=list()
    ContextList=list()
    
      
    #Initialize global data structures 
    
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
    
    #TODO: parse the file with urls and update tags  
    
    
def main():

    
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

