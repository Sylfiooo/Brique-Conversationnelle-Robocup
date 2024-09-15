import spacy
from spacy_wordnet.wordnet_annotator import WordnetAnnotator

# Charger le modèle spaCy pour l'anglais avec l'annotateur WordNet
nlp = spacy.load("en_core_web_md")
nlp.add_pipe("spacy_wordnet", after='tagger') 

# Mot pour lequel vous voulez trouver des synonymes
target_word = "then"

# Obtenir les synonymes du mot cible
synonyms = set()

for word in nlp(target_word):
    for sense in word._.wordnet.synsets():
        for lemma in sense.lemma_names():
            synonyms.add(lemma)

# Afficher les synonymes
print("Synonymes de '{}' : {}".format(target_word, list(synonyms)))