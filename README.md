# cgnenhancer
- A tool for contextualizing news.

- To collaborate, commit to a feature branch.

## How it works
The idea is to provide a simple and smart interface for periodic reviews of your online readings. 

The workflow is the following: (For each session)

1. New links are downloaded from Pocket (for now, this is done manually)
1bis. Tags can be suggested for the newly downloaded links
2. New articles are contextualized (i.e., the user assigns them to contexts, possibly using AI suggestions)
2bis. AI suggests the 'most similar' article inside _that_ context (i.e. AI increases user's long-term memory...)
3. The user can create a new context, and assign articles to them (manually, or using tags)
4. The user can view a context, list the articles it contains, and read them in the browser

## Design principles

The program should:

- store and read the corpus of articles in an efficient (vectorized) way
- be smart enough to result useful

## Implementation
The `class Context` ...

The `class Articles` ...


## Todo

CLI DESIGN:
-----------
- Add unit testing
- Review the design the download of long lists of articles (Efficiency!)
- Refactor the cli using bidict (See utilities.py)
- Refactor the main using some good CLI program as reference
- Add a well-behaved progress bar when loading articles
- Add a list of unreacheable urls
- Add a list of forbidden urls

CLASS ARTICLE
-------------
- Test this class
- Extract text from PDF

CLASS CONTEXT
-------------
- Test this class
- Solve a major flaw in the design: the main program uses a dict to map contexts onto urls, but that should be done using a member of objects of the Context class instead...

MACHINE LEARNING:
-----------------

- Decide what to do with tags (only aggregate manipulation?)
- Recommend articles to contexts
- Compare different learning algorithms as in https://github.com/academia-edu/research_interest_tagger/blob/master/retrain_models.py



WEB:
----
- Use the Pocket's API to download url directly
- Access to FORBIDDEN url (using a browser API, or python-mechanize ?)
- Use Twitter access tokens to improve tweets handling
- Save pages to Wayback when downloading the first time (See the Wiki bot: https://meta.wikimedia.org/wiki/InternetArchiveBot)
