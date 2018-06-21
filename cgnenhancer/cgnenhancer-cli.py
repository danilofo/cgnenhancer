from cgnenhancer import Article, Context, extract_urls, read_contexts_from_txt

###############################################################################
# Main Loop                                                                   #
###############################################################################
def main():
    # Basic init
    exit_flag = False
    settings = Settings()
    # Create the dictionaries for contexts, tag and urls
    contexts_filename = settings.contexts_fname
    url_to_tag, tag_to_url = extract_urls(settings.urls_fname)
    contexts_to_url, url_to_contexts = read_contexts_from_txt(
        contexts_filename)
    # Create the list of Contexts and Articles
    articles = []
    print("Downloading articles:")
    counter = 0
    for art_url in url_to_tag.keys():
        counter += 1
        Article(art_url)
        #progress_bar = "=" * counter
        #print("\t" + progress_bar, end=" ")
    contexts = [Context(c,
                        articles,
                        url_to_tag) for c in contexts_to_url.keys()]
    # Create the last needed dictionary
    url_to_article = {a.url: a for a in articles}
    while not exit_flag:
        # Main menu loop
        print("[*] Cognitive enhancer CLI")
        contexts_mapper = {i + 1: contexts[i] for i in range(len(contexts))}
        print("[+] You want to:")
        print("    (L) List your contexts")
        print("    (A) Add and modify a new context")
        print("    (N) Contextualize last added news")
        print("    (X) Exit")
        context_choice = input("> ")
        if context_choice == "X":
            exit_flag = True
        elif context_choice == "A":
            create_new_context(contexts,
                               contexts_to_url,
                               url_to_article,
                               url_to_contexts,
                               url_to_tag,
                               tag_to_url,
                               settings)
        elif context_choice == "N":
            print("TODO!")
            pass
        elif context_choice == "L":
            lev_spaces = "   "
            print("[+] Available contexts:")
            for k in contexts_mapper.keys():
                print(lev_spaces, k, contexts_mapper[k].name)
            print("Choose a context number or go back (X):")
            context_choice = input("> ")
            if context_choice == "X":
                pass
            elif int(context_choice) in contexts_mapper.keys():
                context_choice = int(context_choice)
                name = contexts_mapper[context_choice]
                current_context = Context(name,
                                          contexts_to_url[name],
                                          url_to_tag)
                back_to_main_menu = False
                while not back_to_main_menu:
                    back_to_main_menu = view_context(current_context,
                                                     contexts_to_url,
                                                     url_to_tag)
        else:
            pass
    return


##############################################################################
# Functionalities                                                            #
##############################################################################
def contextualize_new(articles,
                      contexts,
                      url_to_contexts,
                      contexts_to_url,
                      url_to_tag,
                      tag_to_url):
    """
    Propose contexts for news with not associated with any context

    Arguments
    ---------
    articles: list of Article objs ???
    contexts: list of Context objs
    url_to_contexts: dict
    contexts_to_url: dict
    url_to_tag: dict
    """
    return


def save_contexts(contexts, contexts_to_url, contexts_fname):
    """ Utility to save contexts to file"""
    contexts_ofile = open(contexts_fname)
    for c in contexts:
        for url in contexts_to_url[c.name]:
            print(c.name + " : " + url)
    contexts_ofile.close()


def create_new_context(contexts,
                       contexts_to_url,
                       url_to_article,
                       url_to_contexts,
                       url_to_tag,
                       tag_to_url,
                       settings):
    """
    Create a new context interactively and populate it

    Arguments
    ---------
    articles: list of Article objs
    contexts: list of Context objs
    contexts_to_url: dict
    url_to_contexts: dict
    tag_to_url: dict
    """
    print("[+] Insert the name of the new context:")
    context_name = input("> ")
    articles = list(url_to_article.keys())
    context = Context(context_name,
                      articles,
                      url_to_tag)
    # Add to the list of contexts
    contexts.append(context)
    print("Context " + context_name + " created successfully")
    print("Select a way to populate it:")
    print("   (T) Assign tags to this context")
    print("   (N) Choose from articles without a context")
    print("   (A) Choose from the complete list of articles")
    print("   (Q) Go back and discard changes")
    back_to_prev_menu = False
    while not back_to_prev_menu:
        choice = input("> ")
        if choice == "T":
            print("Available tags:")
            for tag in tag_to_url.keys():
                print(tag)
            print()
            print("Choose a tag names separated by comma (without spaces)")
            print("or exit (X)")
            tag_list = []
            stop_reading = False
            while not stop_reading:
                line = input("> ")
                if line == "X":
                    stop_reading = True
                else:
                    line = line.split(",")
                    for tag_str in line:
                        tag_list.append(tag_str)
                    print("Do you want to add the following articles? N/y")
                    for tag in tag_list:
                        if tag in tag_to_url.keys():
                            print("Tag: " + tag)
                            for url in tag_to_url[tag]:
                                if url in url_to_article.keys():
                                    print(url_to_article[url].title)
                        else:
                            print("[!!!] Invalid tag " + tag)
                    choice = input("> ")
                    if choice == "y":
                        for tag in tag_list:
                            if tag in tag_to_url.keys():
                                for url in tag_to_url[tag]:
                                    if url in url_to_article.keys():
                                        context.add_article(
                                            url_to_article[url])
                        save_contexts(contexts,
                                      contexts_to_url,
                                      settings.contexts_fname)
                        print("[+] Creation completed")
                    else:
                        print("[!] Undo!")
        elif choice == "N":
            print("TODO: NOT YET IMPLEMENTED")
            pass
        elif choice == "A":
            print("TODO: NOT YET IMPLEMENTED")
            pass
        elif choice == "Q":
            back_to_prev_menu = True
    return


def view_context(current_context,
                 contexts_to_url,
                 url_to_tag):
    """
    View current context and its articles

    Arguments
    ---------
    current_context: Context
    contexts_to_url: dict
    url_to_tag: dict

    Return
    ------
    back_to_main_menu: bool, true if user wants to go back
    """
    lev_spaces = "   "
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
        if tag_choice == 'A':
            for art in current_context.articles:
                print("[+++] ", art.title)
                print("     Tags:", url_to_tag[art.url])
                print()
        elif tag_choice == 'Sa':
            suggested_list = []
            print(suggested_list)
        elif tag_choice == 'St':
            for article in current_context.articles:
                print("[+++] ", article.title)
                print("     Tags:", url_to_tag[article.url])
                article.suggest_tags(current_context.articles, url_to_tag)
                print("     Suggested Tags:",
                      article.suggested_tags)
    return back_to_main_menu


class Settings():
    """ Utility to store settings """
    def __init__(self):
        self.contexts_fname = "./contexts.txt"
        self.urls_fname = "./urls.html"


if __name__ == "__main__":
    main()
