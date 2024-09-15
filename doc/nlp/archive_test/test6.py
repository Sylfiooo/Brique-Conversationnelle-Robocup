import spacy

# 'go into the kitchen or into the bathroom'
# 'bring two bananas , a potato and three tacos to Bob and to Cassy'
# 'catch me a beer'

def has_child_number(token):
    # Vérifie si le token a un enfant qui est un nombre
    for child in token.children:
        if child.pos_ == "NUM":
            return child.text
    return None

def recursive_descendants(t, descendants):
    for child in t.children:
        descendants.append(child)
        descendants = recursive_descendants(child, descendants)
    return descendants

# Charger le modèle spaCy
nlp = spacy.load("en_core_web_md")

# Analyser la phrase avec spaCy
doc = nlp('bring two bananas , a potato and three tacos to Bob and to Cassy')

objToReturn = {}

# Trouver le token racine (root)
root_token = next(token for token in doc if token.head == token)

objToReturn['action'] = root_token.text

isParams = False
isPerson = False

# Afficher les enfants directs de la racine
print(f"Enfants directs de la racine ({root_token.text}):")
for child in root_token.children:
    number = None
    print(f"{child.text} <--{child.dep_}/{child.pos_}-- {root_token.text}")

    if child.pos_ == 'NOUN':
        number = has_child_number(child)

        objToAdd = {'name': child.text}
        if number != None: objToAdd['number'] = number

        if isParams == True: objToReturn['params'].append(objToAdd)
        else:
            objToReturn['params'] = [objToAdd]
            isParams = True
        number = None

        descendants = recursive_descendants(child, [])
        print(descendants)
        for descendant in descendants:
            print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)  
            if descendant.pos_ in ['NOUN']: 
                number = has_child_number(descendant)

                objToAdd = {'name': descendant.text}
                if number != None: objToAdd['number'] = number
                objToReturn['params'].append(objToAdd)

    
    if child.pos_ in ['PRON', 'PROPN'] :
        if isPerson == True:
            objToReturn['person'].append(child.text)
        else:
            objToReturn['person'] = [child.text]
            isPerson = True
        descendants = recursive_descendants(child, [])
        print(descendants)
        for descendant in descendants:
            print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)  
            if descendant.pos_ in ['PRON', 'PROPN']:
                objToReturn['person'].append(descendant.text)
            
    if child.pos_ == 'ADP':
        objToReturn[child.text] = []
        descendants = recursive_descendants(child, [])
        print(descendants)
        for descendant in descendants:
            print(descendant.text, descendant.dep_, descendant.pos_, descendant.head.text)  
            if descendant.pos_ in ['NOUN', 'PROPN', 'PRON']:
                objToReturn[child.text].append(descendant.text)

print(objToReturn)

for token in doc:
    print(token.text, token.pos_, token.dep_, token.head.text)
