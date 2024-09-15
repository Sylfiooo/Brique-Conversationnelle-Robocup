from word2number import w2n
import re

def convertir_nombres_en_chiffres(phrase):
    mots = phrase.split()
    nouvelle_phrase = []

    for mot in mots:
        # Vérifier si le mot est un nombre écrit en lettres
        if re.match(r'^[a-zA-Z]+$', mot):
            try:
                # Convertir le mot en chiffre
                nombre_chiffre = w2n.word_to_num(mot)
                nouvelle_phrase.append(str(nombre_chiffre))
            except ValueError:
                # Si la conversion échoue, ajouter le mot tel quel
                nouvelle_phrase.append(mot)
        else:
            # Si ce n'est pas un nombre écrit en lettres, ajouter le mot tel quel
            nouvelle_phrase.append(mot)

    # Rejoindre les mots pour former la nouvelle phrase
    nouvelle_phrase = ' '.join(nouvelle_phrase)
    return nouvelle_phrase

# Exemple d'utilisation
phrase_originale = "I go to Paris where i seen three thousand two hundred and fifty beers, then i go to London and i live at five PM"
phrase_convertie = convertir_nombres_en_chiffres(phrase_originale)
print(phrase_convertie)