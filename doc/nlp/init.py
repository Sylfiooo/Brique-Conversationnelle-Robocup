import spacy
from word2number import w2n
from random import choice, randint

modelSpaCy = "en_core_web_md"

'''
    Fonction qui permet de créer une phrase à partir d'un ordre formaté

    @param objectFormatted: L'ordre formaté
    @return sentence: La phrase créée
'''
def sentenceCreator(objectFormatted, debug = False):
    if debug : print("##############\n", "DEBUT DE LA CREATION DE LA PHRASE\n", "##############\n")
    nlp = spacy.load(modelSpaCy)

    randomStart = ["I need to", "I have to", "I must"]

    sentence = "so "

    def concatener_sentence(tableau):

        randomConcat = ["then", "and then", "and after", "and after that", "and then after", "and"]

        # Utiliser la méthode join pour concaténer les chaînes avec un élément aléatoire de randomConcat au milieu
        resultat = ""
        i = 0
        for mot in tableau:
            if i != len(tableau) - 1:
                resultat += mot + " " + choice(randomConcat) + " "
            else: resultat += mot
            i += 1

        return resultat

    cles_a_exclure = ["action", "person", "params"]

    sentenceTab = []

    for order in objectFormatted:
        current_sentence = ""
        if debug : print("##############\n", order)
        current_sentence += randomStart[randint(0, len(randomStart) - 1)] + " " + order["action"]

        # PERSON
        if 'person' in order:
            tabPerson = order['person']
            tableau_modifie = [phrase.replace("you", "temp").replace("me", "you").replace("temp", "me") for phrase in tabPerson]
            if len(tableau_modifie) > 2: current_sentence += ", ".join(tableau_modifie[:-1]) + " and " + tableau_modifie[-1]
            else : current_sentence += " " + " and ".join(tableau_modifie)

        # PARAMS
        if 'params' in order:
            tabParams = order['params']
            tabParamsFormatted = []
            for param in tabParams:
                paramFormatted = ""
                doc = nlp(param['name'])
                if doc[0].pos_ == "NOUN":
                    if 'number' in param: paramFormatted += str(param['number']) + " " + param['name']
                    else : paramFormatted += "the " + param['name']
                else : paramFormatted += param['name']

                tabParamsFormatted.append(paramFormatted)

            if len(tabParamsFormatted) > 2: current_sentence += " " + ", ".join(tabParamsFormatted[:-1]) + " and " + tabParamsFormatted[-1]
            else : current_sentence += " " + " and ".join(tabParamsFormatted)

        cles_non_exclues = [cle for cle in order.keys() if cle not in cles_a_exclure]

        for cle in cles_non_exclues:
            tabKey = order[cle]
            tabKeyYou = [phrase.replace("you", "temp").replace("me", "you").replace("temp", "me") for phrase in tabKey]
            tabKeyFormatted = []

            for key in tabKeyYou:
                keyFormatted = ""
                doc = nlp(key)
                if doc[0].pos_ == "NOUN": keyFormatted += "the " + key
                else : keyFormatted += key
                tabKeyFormatted.append(keyFormatted)

            if len(tabKeyFormatted) > 2: current_sentence += " " + cle + ", ".join(tabKeyFormatted[:-1]) + " and " + tabKeyFormatted[-1]
            else : current_sentence +=  " " + cle + " " + " and ".join(tabKeyFormatted)

            if debug : print(current_sentence) 

        if debug : print(cles_non_exclues)

        sentenceTab.append(current_sentence)

    sentence += concatener_sentence(sentenceTab) + " ?"
    return sentence

'''
    Fonction qui permet de séparer une phrase en sous-phrases
    en fonction des conjonctions de coordination (par exemple, "and")
    
    @param sentence: la phrase à séparer
    @return subphrases: la liste des sous-phrases
'''
def sentenceSplitter(sentence, debug = False):

    def convertir_minuscules_sauf_noms_propres(phrase):
        nlp = spacy.load(modelSpaCy)
        
        # Analyser la phrase
        doc = nlp(phrase)
        
        # Convertir en minuscules tous les mots qui ne sont pas des noms propres
        mots_modifies = [token.text.lower() if token.ent_type_ == "" else token.text for token in doc]
        
        # Rejoindre les mots pour former la phrase modifiée
        phrase_modifiee = ' '.join(mots_modifies)

        print(phrase_modifiee)
        
        return phrase_modifiee

    nlp = spacy.load(modelSpaCy) # Charger le modèle spaCy

    doc = nlp(convertir_minuscules_sauf_noms_propres(sentence)) # On crée notre doc 

    subphrases = [] # Création du tableau de sous-phrases

    adverb_list = ["then"] # Définir la liste des mots alternatifs
    indStart = 0

    # Parcourir les tokens dans la phrase
    for token in doc:
        wordBreaker = False # Vérificateur de séparation de sous-phrase

        if debug : print(token.text, token.pos_, token.dep_, token.head.text)

        if (token.pos_ == 'CCONJ' or token.pos_ == 'PUNCT') and token.head.pos_ == 'VERB': # Si le token est un cc lié à un verbe (pour un autre verbe  )
            wordBreaker = True

        elif token.pos_ == "ADV" and (token.text.lower() in adverb_list):
            wordBreaker = True

        if wordBreaker == True:
            # Ajouter la sous-phrase actuelle à la liste
            strTab = ' '.join([t.text for t in doc[indStart:token.i]]).strip()

            if strTab not in ['', ' ']: subphrases.append(strTab)
            # Réinitialiser la sous-phrase pour la suivante
            indStart = token.i + 1

    # Ajouter la dernière sous-phrase à la liste
    strTab = ' '.join([t.text for t in doc[indStart:]]).strip()
    if strTab not in ['', ' '] : subphrases.append(strTab)

    return subphrases

'''
    Fonction qui permet de formater l'ordre reçu sous en forme contenant les informations essentielles

    @param sentence: L'ordre à formater
    @return objectFormatted: L'ordre format
'''
def orderFormatter(sentence, debug = False):
    nlp = spacy.load(modelSpaCy) # Charger le modèle spaCy

    doc = nlp(sentence) # On crée notre doc

    objectFormatted = {} # Création de l'objet de retour

    root_token = next(token for token in doc if token.head == token) # Trouver le token racine (root)

    def replace_with_verb(root_token):
        # Parcourez les enfants du token racine
        for child in root_token.children:
            # Si l'enfant est un verbe, remplacez le token racine par cet enfant
            if child.pos_ == "VERB":
                return child
        # Si aucun enfant n'est un verbe, retournez le token racine d'origine
        return root_token

    root_token = replace_with_verb(root_token) # Remplacer le token racine par un verbe

    objectFormatted['action'] = root_token.text

    def get_child_number(token):
        # Vérifie si le token a un enfant qui est un nombre
        for child in token.children:
            if child.pos_ == "NUM":
                return w2n.word_to_num(child.text)
        return None

    def recursive_descendants(t, descendants):
        for child in t.children:
            descendants.append(child)
            descendants = recursive_descendants(child, descendants)
        return descendants
    
    isParams = False
    isPerson = False

    if debug : 
        for child in doc:
            print(child.text, child.dep_, child.pos_, child.head.text)
        print(f"Enfants directs de la racine ({root_token.text}):")
    for child in root_token.children:

        if debug: print(f"{child.text} <--{child.dep_}/{child.pos_}-- {root_token.text}")

        # ADP
        if child.pos_ == 'ADP':
            objectFormatted[child.text] = []
            childDescendants = recursive_descendants(child, [])
            if debug: print(childDescendants)
            for descendant in childDescendants:
                if debug: print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)
                if descendant.pos_ in ['NOUN', 'PROPN', 'PRON']:
                    objectFormatted[child.text].append(descendant.text)
        
        # PERSON
        if (child.pos_ == 'PRON' and child.dep_ == 'dative') or child.pos_ == 'PROPN' :
            if isPerson: objectFormatted['person'].append(child.text)
            else: objectFormatted['person'] = [child.text]
            isPerson = True
            childDescendants = recursive_descendants(child, [])
            if debug: print(childDescendants)
            for descendant in childDescendants:
                if debug: print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)
                if descendant.pos_ in ['PRON', 'PROPN']:
                    objectFormatted['person'].append(descendant.text)

        # PARAMS
        if child.pos_ == 'NOUN' or (child.pos_ == 'PRON' and child.dep_ == 'dobj') :
            number = get_child_number(child)
            objToAdd = {'name': child.text}
            if number != None: 
                objToAdd['number'] = number
            elif child.pos_ == 'NOUN': 
                for childChild in child.children:
                    if childChild.text.lower() in ["a", "an"]:
                        objToAdd['number'] = 1

            if isParams: objectFormatted['params'].append(objToAdd)
            else: objectFormatted['params'] = [objToAdd]
            isParams = True
            number = None

            childDescendants = recursive_descendants(child, [])
            if debug: print(childDescendants)
            for descendant in childDescendants:
                if debug: print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)
                if descendant.pos_ in ['NOUN', 'PROPN', 'PRON']:
                    number = get_child_number(descendant)
                    objToAdd = {'name': descendant.text}
                    if number != None: objToAdd['number'] = number
                    elif descendant.pos_ == 'NOUN': 
                        for childChild in descendant.children:
                            if childChild.text.lower() in ["a", "an"]:
                                objToAdd['number'] = 1
                    objectFormatted['params'].append(objToAdd)

    return objectFormatted


if __name__ == "__main__":
    testSentenceSplited = sentenceSplitter("put the knife on the table and return in the bathroom")
    print(testSentenceSplited)
    tabFormated = []
    for subSentence in testSentenceSplited:
        orderFormated = orderFormatter(subSentence)
        tabFormated.append(orderFormated)
    print(tabFormated)
    print(sentenceCreator(tabFormated))
    