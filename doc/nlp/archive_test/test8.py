import spacy
from spacy.matcher import Matcher
from word2number import w2n

def custom_word_to_num(text):
    # Gestion des préfixes spéciaux (par exemple, hundred, thousand)
    special_prefixes = {
        "hundred": 100,
        "thousand": 1000,
        "million": 1000000,
        # Ajoutez d'autres préfixes au besoin
    }

    # Utilisez la fonction word_to_num de word2number
    number = w2n.word_to_num(text)

def extract_info(text):
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(text)

    matcher = Matcher(nlp.vocab)
    pattern = [{"POS": "NUM"}, {"POS": "NOUN"}]
    matcher.add("Number-Noun", [pattern])

    matches = matcher(doc)

    result = {}
    for match_id, start, end in matches:
        number_token = doc[start]
        noun_token = doc[end - 1]
        result["name"] = noun_token.text
        result["number"] = custom_word_to_num(number_token.text)
        break  # Assume only one match for simplicity, you may adjust this logic based on your needs

    return result

# Example usage:
text = "three thousand two hundred and fifty"
print(w2n.word_to_num(text))