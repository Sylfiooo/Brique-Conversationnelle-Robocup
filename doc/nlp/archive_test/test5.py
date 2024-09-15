import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator 

import nltk
nltk.download('wordnet')

# Load a spaCy model (supported languages are "es" and "en") 
nlp = spacy.load('en_core_web_md')
# spaCy 3.x
nlp.add_pipe("spacy_wordnet", after='tagger')
# spaCy 2.x
# nlp.add_pipe(WordnetAnnotator(nlp.lang), after='tagger')
token = nlp('prices')[0]

# WordNet object links spaCy token with NLTK WordNet interface by giving access to
# synsets and lemmas 
token._.wordnet.synsets()
token._.wordnet.lemmas()

# And automatically add info about WordNet domains
token._.wordnet.wordnet_domains()


