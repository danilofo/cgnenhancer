from cgnenhancer import Article, Context, extract_urls, read_contexts_from_txt


###############################################################################
# Main Loop                                                                   #
###############################################################################
def main():
    contexts_filename = "./contexts.txt"
    lev_spaces = "   "
    exit_flag = False
    url_to_tag, tag_to_url = extract_urls("./urls.html")
    contexts_to_url, url_to_contexts = read_contexts_from_txt(
        contexts_filename)
    contexts = list(contexts_to_url.keys())
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
                                      contexts_to_url[name],
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
                    articles = [Article(art_url) for art_url
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
