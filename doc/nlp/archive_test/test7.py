import spacy
from word2number import w2n

def convert_written_numbers_to_digits(text):
    # Charger le modèle spaCy pour l'anglais
    nlp = spacy.load("en_core_web_sm")

    # Traitement de la phrase avec spaCy
    doc = nlp(text)

    # Convertir les nombres écrits en nombres chiffrés
    converted_text = []
    for token in doc:
        if token.pos_ == "NUM" and token.text.isalpha():
            # Si le token est un nombre écrit, le convertir
            converted_text.append(str(w2n.word_to_num(token.text)))
        else:
            converted_text.append(token.text)

    return " ".join(converted_text)

# Exemple d'utilisation
text_with_written_numbers = "There are fifteen apples and twenty-seven oranges."
converted_text = convert_written_numbers_to_digits(text_with_written_numbers)
print("Texte d'origine :", text_with_written_numbers)
print("Texte converti :", converted_text)