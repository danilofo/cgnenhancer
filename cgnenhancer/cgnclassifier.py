'''
Created on 24 apr 2017

@author: danilo
'''

#The machine learning environment is the SciKit Learn package
from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

class TextClassifier:
    '''
    One object of this class is instanciated each time a context is opened;
    It compares articles in the current context
    '''

    def __init__(self, CurrentContext):
        '''
        Constructor
        '''
        #TODO: obtain the urls relative to this context
        
        #TODO: open the urls and parse the html 
        
        #TODO: construct the tf-idf matrix
        
    def findSimilar(self,CurrentArticleID):
        #TODO: return the distance of other articles from the current one
        
        
        
        