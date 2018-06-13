import urllib
from bs4 import BeautifulSoup

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
                 articles_db):
        assert isinstance(name, str)
        assert isinstance(articles, list)
        # A context contains articles and tags
        self.name = name
        self.articles = articles
        self.tags = []
        for art in articles:
            for tag in articles_db[art]:
                if tag not in self.tags:
                    self.tags.append(tag)

    def addArticle(self, myArticle):
        assert isinstance(myArticle, Article)
        if myArticle not in self.articles:
            self.articles.append(myArticle)
        for tag in myArticle.tags:
            if tag not in self.tags:
                self.tags.append(tag)


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
            # NOTE: learning is performed assigning a binary vector (a category)
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
            label_vectors = [
                [1 if t in url_to_tag[article.url] else 0
                 for t in tags]
                for article in article_list]
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
            suggested_tags = multiclass_clf.predict_proba(tfidf_this_article)
            print(suggested_tags)
            # for tag in suggested_tags:
            #    if tag not in url_to_tag[self.url]:
            #        self.suggested_tags.append(tag)


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
    context_dict = {}
    for line in open(fname):
        context_name, url = line.split(":", 1)
        if context_name not in context_dict.keys():
            context_dict[context_name] = list()
        if url not in context_dict[context_name]:
            url = url.strip("\n").strip(" ")
            context_dict[context_name].append(url)
    return context_dict


###############################################################################
# Main Loop                                                                   #
###############################################################################
def main():
    contexts_filename = "./contexts.txt"
    lev_spaces = "   "
    exit_flag = False
    url_to_tag, tag_to_url = extract_urls("./urls.html")
    contexts_dict = read_contexts_from_txt(contexts_filename)
    contexts = list(contexts_dict.keys())
    while not exit_flag:
        # Main menu loop
        print("[*] Cognitive enhancer debug version")
        contexts_mapper = {i + 1: contexts[i] for i in range(len(contexts))}
        print("[+] Available contexts:")
        for k in contexts_mapper.keys():
            print(lev_spaces, k, contexts_mapper[k])
        print("[+] Choose a context number or exit (X):")
        context_choice = input("> ")
        # TODO: parse ContextChoice variable
        if context_choice == "X":
            exit_flag = True
        elif int(context_choice) in contexts_mapper.keys():
            context_choice = int(context_choice)
            name = contexts_mapper[context_choice]
            current_context = Context(name,
                                      contexts_dict[name],
                                      url_to_tag)
            back_to_main_menu = False
            while not back_to_main_menu:
                print("Context: " + current_context.name)
                # TODO: print the list of available tags
                print("[++] Actions:")
                print(2*lev_spaces, "List articles (A)")
                print(2*lev_spaces,
                      "Suggest articles for the current context (Sa)")
                print(2*lev_spaces,
                      "Suggest tags for articles in the current context (St)")
                print(2*lev_spaces, "Go back to the previous menu (Q)")
                tag_choice = input("> ")
                actions = ['Q', 'A', 'Sa', 'St']
                if tag_choice == 'Q':
                    back_to_main_menu = True
                elif tag_choice in actions:
                    articles = [Article(art_url, ) for art_url
                                in current_context.articles]
                    if tag_choice == 'A':
                        for art in articles:
                            print("[+++] ", art.title)
                            print("     Tags:", url_to_tag[art.url])
                            print()
                    elif tag_choice == 'Sa':
                        suggested_list = []
                        print(suggested_list)
                    elif tag_choice == 'St':
                        for article in articles:
                            print("[+++] ", article.title)
                            print("     Tags:", url_to_tag[article.url])
                            article.suggest_tags(articles, url_to_tag)
                            print("     Suggested Tags:",
                                  article.suggested_tags)
                else:
                    pass
        else:
            pass
    return


if __name__ == "__main__":
    main()
