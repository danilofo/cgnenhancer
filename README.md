# cgnenhancer
- A tool for contextualizing news.

- To collaborate, commit to a feature branch.

## Todo

CLI DESIGN:
-----------
- Review the design the download of long lists of articles (Efficiency!)
- Refactor the cli using bidict (See utilities.py)
- Refactor the main using some good CLI program as reference
- Add a well-behaved progress bar when loading articles
- Add a list of unreacheable urls
- Add a list of forbidden urls

CLASS ARTICLE
-------------
- Extract text from PDF

CLASS CONTEXT
-------------
- Solve a major flaw in the design: the main program uses a dict to map contexts onto urls, but that should be done using a member of objects of the Context class instead...

MACHINE LEARNING:
-----------------

- Decide what to do with tags (only aggregate manipulation?)
- Recommend articles to contexts
- Compare different learning algorithms as in https://github.com/academia-edu/research_interest_tagger/blob/master/retrain_models.py



WEB:
----
- Access to FORBIDDEN url (using a browser API, or python-mechanize ?)
- Use Twitter access tokens to improve tweets handling
- Save pages to Wayback when downloading the first time
