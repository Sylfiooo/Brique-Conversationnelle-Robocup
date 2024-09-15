import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_md')



# Texte récupéré par STT (Speech-to-Text)
texte_instruction = "go to the kitchen and bring a banana to Bob"
#texte_instruction = "va à la cuisine et ramène une banane à Bob"

# Traiter le texte avec spaCy
doc = nlp(texte_instruction)

# Extraire les entités nommées basées sur la partie du discours
entites = [(entite.text, entite.pos_) for entite in doc if entite.ent_type_ != "" or entite.pos_ != ""]

print("Entitées totales:", entites)

# Filtrer les entités par celles qui sont des noms communs (NOUN)
entites_filtrees = [(texte, pos) for texte, pos in entites if pos == "NOUN"]

# Afficher les entités identifiées
print("Entités identifiées:", entites_filtrees)

# Extraire les verbes et leurs objets directs
actions = []
for token in doc:
    if token.pos_ == "VERB":
        action = token.text
        # Trouver d'autres éléments associés au verbe (pouvant être une localisation ou une personne)
        autres_elements = [descendant.text for descendant in token.subtree]
        actions.append((action, autres_elements))

# Afficher les actions identifiées
print("Actions identifiées:", actions)
