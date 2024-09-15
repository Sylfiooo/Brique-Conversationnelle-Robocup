from word2number import w2n
import re

def convertir_nombres_en_chiffres(phrase):
    mots = re.findall(r'\b\w+\b|[.,;!?]', phrase)
    print(mots)
    nouvelle_phrase = []
    nombre_en_cours = ""

    for mot in mots:
        if re.match(r'^[a-zA-Z]+$', mot):
            print(nombre_en_cours)
            # Si le mot est alphabétique, concaténer pour former un nombre en cours
            nombre_en_cours += mot + " "
        else:
            # Si nous avons un nombre en cours, convertir et ajouter à la nouvelle phrase
            if nombre_en_cours.strip():
                try:
                    nombre_chiffre = w2n.word_to_num(nombre_en_cours.strip())
                    nouvelle_phrase.append(str(nombre_chiffre))
                except ValueError:
                    # Si la conversion échoue, ajouter le mot original
                    nouvelle_phrase.append(nombre_en_cours.strip())
            else:
                # Si ce n'est pas un nombre écrit en lettres, ajouter le mot tel quel
                nouvelle_phrase.append(mot)
                
            # Réinitialiser le nombre en cours
            nombre_en_cours = ""

    # Rejoindre les mots pour former la nouvelle phrase
    nouvelle_phrase = ''.join(nouvelle_phrase)
    return nouvelle_phrase

# Exemple d'utilisation
phrase_originale = "I go to Paris where i seen three thousand two hundred and fifty beers, then i go to London and i live at five PM"
phrase_convertie = convertir_nombres_en_chiffres(phrase_originale)
print(phrase_convertie)