import spacy

# Charger le modèle spaCy pour l'anglais
nlp = spacy.load("en_core_web_md")

# Phrase d'exemple
text = "Firstly, let's start immediatly with an introduction. Then, we can move on to the main topic. Finally, we'll conclude."

# Traitement de la phrase avec spaCy
doc = nlp(text)

# Identifier les conjonctions et adverbes de coordination
separator_words = [token.text for token in doc if token.dep_ in ('cc', 'advmod')]

# Afficher les mots séparateurs identifiés
print("Mots séparateurs identifiés :", separator_words)