import spacy

def split_sentence(input_sentence):
    # Charger le modèle spaCy
    nlp = spacy.load("en_core_web_md")

    # Analyser la phrase avec spaCy
    doc = nlp(input_sentence)

    # Initialiser une liste pour stocker les sous-phrases
    subphrases = []
    current_subphrase = []

    # Parcourir les tokens dans la phrase
    for token in doc:
        # Si le token est une conjonction de coordination (par exemple, "and")
        if token.dep_ == 'cc':
            # Ajouter la sous-
            # phrase actuelle à la liste
            if current_subphrase:
                subphrases.append(' '.join([t.text for t in current_subphrase]).strip())
                current_subphrase = []
        else:
            # Ajouter le token à la sous-phrase actuelle
            current_subphrase.append(token)

    # Ajouter la dernière sous-phrase à la liste
    if current_subphrase:
        subphrases.append(' '.join([t.text for t in current_subphrase]).strip())

    for token in doc:
        print(token.text, token.pos_, token.dep_, token.head.text)
    return subphrases

# Exemple d'utilisation
input_sentence = "go to kitchen immediatly then bring two bananas and a potato to Bob and catch me a beer"
output = split_sentence(input_sentence)


print(output)