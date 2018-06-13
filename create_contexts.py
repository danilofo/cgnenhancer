url_to_tag = dict()
url_list = open("urls.html", 'r')
context_file = open("contexts.txt", "w")
# builds a dictionary with urls as keys and tags as values
for line in url_list:
    junk_line, line = line.split("=", 1)
    url, line = line.split(" ", 1)
    url = url.strip('"')
    str_to_write = "context1: " + url + "\n"
    context_file.write(str_to_write)
#
url_list.close()
context_file.close()
