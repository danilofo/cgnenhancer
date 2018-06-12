import urllib
from bs4 import BeautifulSoup


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
        # the option lxml avoids a warning
        html = urllib.request.urlopen(url)
        page = BeautifulSoup(html.read(), "lxml")
        self.title = page.title.string
        self.preview = ""


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
                        print
                else:
                    pass
        else:
            pass
    return


if __name__ == "__main__":
    main()
