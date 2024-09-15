import json
from random import choice, randint
from word2number import w2n
import spacy

class NlpAlgorithm:
    def __init__(self, debug=False):
        self.modelSpacy = "en_core_web_md"
        self.debug = debug
        self.nlp = spacy.load(self.modelSpacy)

    def concatener_sentence(self, tableau):

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

    def generate_sentence(self, objects_formatted):
        if self.debug : print("##############\n", "DEBUT DE LA CREATION DE LA PHRASE\n", "##############\n")

        randomStart = ["I need to", "I have to", "I must"]

        sentence = "so "

        cles_a_exclure = ["action", "person", "params"]

        sentenceTab = []

        objects_string_formatted = objects_formatted

        objects_formatted = [json.loads(element) for element in objects_string_formatted]

        for order in objects_formatted:
            current_sentence = ""
            if self.debug : print("##############\n", order)
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
                    doc = self.nlp(param['name'])

                    if 'number' in param: paramFormatted += str(param['number']) + " " + param['name']
                    elif doc[0].pos_ == "NOUN": paramFormatted += "the " + param['name']
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
                    doc = self.nlp(key)
                    if doc[0].pos_ == "NOUN": keyFormatted += "the " + key
                    else : keyFormatted += key
                    tabKeyFormatted.append(keyFormatted)

                if len(tabKeyFormatted) > 2: current_sentence += " " + cle + ", ".join(tabKeyFormatted[:-1]) + " and " + tabKeyFormatted[-1]
                else : current_sentence +=  " " + cle + " " + " and ".join(tabKeyFormatted)

                if self.debug : print(current_sentence) 

            if self.debug : print(cles_non_exclues)

            sentenceTab.append(current_sentence)

        sentence += self.concatener_sentence(sentenceTab) + " ?"

        return sentence
    
    def split_sentence(self, sentence):
        doc = self.nlp(self.convertir_minuscules_sauf_noms_propres(sentence)) # On crée notre doc 

        subphrases = [] # Création du tableau de sous-phrases

        adverb_list = ["then"] # Définir la liste des mots alternatifs
        indStart = 0

        # Parcourir les tokens dans la phrase
        for token in doc:
            wordBreaker = False # Vérificateur de séparation de sous-phrase

            if self.debug : print(token.text, token.pos_, token.dep_, token.head.text)

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
        if self.debug : print(subphrases)

        return subphrases

    def convertir_minuscules_sauf_noms_propres(self, phrase):
        # Analyser la phrase
        doc = self.nlp(phrase)
        
        # Convertir en minuscules tous les mots qui ne sont pas des noms propres
        mots_modifies = [token.text.lower() if token.ent_type_ == "" else token.text for token in doc]
        
        # Rejoindre les mots pour former la phrase modifiée
        phrase_modifiee = ' '.join(mots_modifies)

        if self.debug: print(phrase_modifiee)
            
        return phrase_modifiee
    
    def replace_with_verb(self, root_token):
        # Parcourez les enfants du token racine
        for child in root_token.children:
            # Si l'enfant est un verbe, remplacez le token racine par cet enfant
            if child.pos_ == "VERB":
                return child
        # Si aucun enfant n'est un verbe, retournez le token racine d'origine
        return root_token

    def get_child_number(self, token):
        # Vérifie si le token a un enfant qui est un nombre
        for child in token.children:
            if child.pos_ == "NUM":
                return w2n.word_to_num(child.text)
        return None

    def recursive_descendants(self, t, descendants):
        for child in t.children:
            descendants.append(child)
            descendants = self.recursive_descendants(child, descendants)
        return descendants
    
    def format_order(self, sentence):
        doc = self.nlp(sentence) # On crée notre doc

        object_formatted = {} # Création de l'objet de retour

        root_token = next(token for token in doc if token.head == token) # Trouver le token racine (root)

        root_token = self.replace_with_verb(root_token) # Remplacer le token racine par un verbe

        object_formatted['action'] = root_token.text
        
        isParams = False
        isPerson = False

        if self.debug : 
            for child in doc:
                print(child.text, child.dep_, child.pos_, child.head.text)
            print(f"Enfants directs de la racine ({root_token.text}):")
        
        for child in root_token.children:

            if self.debug: print(f"{child.text} <--{child.dep_}/{child.pos_}-- {root_token.text}")

            # ADP
            if child.pos_ == 'ADP':
                object_formatted[child.text] = []
                childDescendants = self.recursive_descendants(child, [])
                if self.debug: print(childDescendants)
                for descendant in childDescendants:
                    if self.debug: print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)
                    if descendant.pos_ in ['NOUN', 'PROPN', 'PRON']:
                        object_formatted[child.text].append(descendant.text)
            
            # PERSON
            if (child.pos_ == 'PRON' and child.dep_ == 'dative') or child.pos_ == 'PROPN' :
                if isPerson: object_formatted['person'].append(child.text)
                else: object_formatted['person'] = [child.text]
                isPerson = True
                childDescendants = self.recursive_descendants(child, [])
                if self.debug: print(childDescendants)
                for descendant in childDescendants:
                    if self.debug: print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)
                    if descendant.pos_ in ['PRON', 'PROPN']:
                        object_formatted['person'].append(descendant.text)

            # PARAMS
            if child.pos_ == 'NOUN' or (child.pos_ == 'PRON' and child.dep_ == 'dobj') :
                number = self.get_child_number(child)
                objToAdd = {'name': child.text}
                if number != None: 
                    objToAdd['number'] = number
                elif child.pos_ == 'NOUN': 
                    for childChild in child.children:
                        if childChild.text.lower() in ["a", "an"]:
                            objToAdd['number'] = 1

                if isParams: object_formatted['params'].append(objToAdd)
                else: object_formatted['params'] = [objToAdd]
                isParams = True
                number = None

                childDescendants = self.recursive_descendants(child, [])
                if self.debug: print(childDescendants)
                for descendant in childDescendants:
                    if self.debug: print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)
                    if descendant.pos_ in ['NOUN', 'PROPN', 'PRON']:
                        number = self.get_child_number(descendant)
                        objToAdd = {'name': descendant.text}
                        if number != None: objToAdd['number'] = number
                        elif descendant.pos_ == 'NOUN': 
                            for childChild in descendant.children:
                                if childChild.text.lower() in ["a", "an"]:
                                    objToAdd['number'] = 1
                        object_formatted['params'].append(objToAdd)
        
        return json.dumps(object_formatted)