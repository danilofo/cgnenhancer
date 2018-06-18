import urllib
from bs4 import BeautifulSoup

import numpy

from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.multiclass import OneVsRestClassifier


###############################################################################
# Class for contexts                                                          #
###############################################################################
class Context:
    # A class for the Context data structure;
    # A Context is a container for Articles
    def __init__(self,
                 name,
                 articles,
                 articles_dict):
        assert isinstance(name, str)
        assert isinstance(articles, list)
        # A context contains articles and tags
        self.name = name
        self.articles = articles
        self.articles_dict = articles_dict
        self.tags = []
        for art in articles:
            for tag in self.articles_dict[art]:
                if tag not in self.tags:
                    self.tags.append(tag)

    def add_article(self, my_article):
        assert isinstance(my_article, Article)
        if my_article not in self.articles:
            self.articles.append(my_article)
        for tag in self.articles_dict[my_article.url]:
            if tag not in self.tags:
                self.tags.append(tag)

    def suggest_articles(self):
        """TODO """
        return


###############################################################################
# Class for articles                                                          #
###############################################################################
class Article:
    def __init__(self, url):
        assert isinstance(url, str)
        self.url = url
        self.loaded = False
        self.title = ""
        self.content = ""
        self.suggested_tags = []
        try:
            self.loaded = True
            html = urllib.request.urlopen(url)
            self.page = BeautifulSoup(html.read(), 'lxml')
            if self.page.title is not None:
                self.title = self.page.title.string
            # Basic web scraping procedure
            # Should be refined using information on the single site!
            for x in self.page.find_all("p"):
                for i in x.contents:
                    if i.string is not None:
                        self.content += i.string
        except urllib.error.URLError as e:
            print("Unable to open url", url)
            print("Error: ", e.reason)
            pass

    def suggest_tags(self, article_list, url_to_tag):
        if self.loaded is not False:
            # lists for learning
            # NOTE: learning is performed assigning a binary vector
            # to each text. A 1 in the i-th position means that the article was
            # tagged using the i-th tag
            tags = []
            texts = []
            for article in article_list:
                for tag in url_to_tag[article.url]:
                    if tag not in tags:
                        tags.append(tag)
                texts.append(article.content)
            # Generate one feature vector for each text
            label_vectors = numpy.array([
                [1 if t in url_to_tag[article.url] else 0
                 for t in tags]
                for article in article_list])
            # vectorizer setup
            pattern = '(?u)\\b[A-Za-z]{3,}'
            # TODO: correct classification of italian articles
            cv = CountVectorizer(max_df=0.95,
                                 min_df=0.01,
                                 stop_words='english',
                                 token_pattern=pattern,
                                 ngram_range=(1, 3))
            cv_corpus = cv.fit_transform(texts)
            tfidf = TfidfTransformer(sublinear_tf=True)
            # tf idf matrix: (articles x words)
            tfidf_train_matrix = tfidf.fit_transform(cv_corpus)
            classifier = LinearSVC()
            multiclass_clf = OneVsRestClassifier(classifier)
            multiclass_clf.fit(tfidf_train_matrix, label_vectors)
            # create the matrix for the current article
            cv_this_article = cv.transform([self.content])
            tfidf_this_article = tfidf.transform(cv_this_article)
            #
            suggested_tags = multiclass_clf.predict(tfidf_this_article)
            print(suggested_tags)


###############################################################################
# Utilities                                                                   #
###############################################################################
def extract_urls(namefile):
    url_to_tag = dict()
    url_list = open(namefile, 'r')
    # builds a dictionary with urls as keys and tags as values
    for line in url_list:
        junk_line, line = line.split("=", 1)
        url, line = line.split(" ", 1)
        url = url.strip('"')
        junk_line, line = line.split("tags=")
        tags, junk_line = line.split(">", 1)
        tags = tags.strip('"')
        tag_list = tags.split(",")
        url_to_tag[url] = tag_list
    #
    url_list.close()
    # initialize the dictionary with tags as keys and urls as values
    tag_to_url = {}
    for key in url_to_tag:
        for tag in url_to_tag[key]:
            tag_to_url[tag] = list()
    # add the urls to each tag
    for key in url_to_tag:
        for tag in url_to_tag[key]:
            tag_to_url[tag].append(key)
    return url_to_tag, tag_to_url


def read_contexts_from_txt(fname):
    assert isinstance(fname, str)
    # Parse the file with context and urls
    context_to_url = {}
    url_to_contexts = {}
    for line in open(fname):
        context_name, url = line.split(":", 1)
        url = url.strip("\n").strip(" ")
        if context_name not in context_to_url.keys():
            context_to_url[context_name] = list()
        if url not in url_to_contexts.keys():
            url_to_contexts[url] = []
        if url not in context_to_url[context_name]:
            context_to_url[context_name].append(url)
        if context_name not in url_to_contexts[url]:
            url_to_contexts[url].append(context_name)
    return context_to_url, url_to_contexts


def write_contexts_to_txt(fname, context_to_url):
    assert isinstance(fname, str)
    assert isinstance(context_to_url, dict)
    ofile = open(fname, "w")
    for k in context_to_url.keys():
        for url in context_to_url[k]:
            ofile.write("{}: {}".format(context_to_url[k], url))
    ofile.close()
    return
