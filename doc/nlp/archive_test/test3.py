import spacy
nlp = spacy.load("en_core_web_md")

# Compare two documents
doc = nlp("Go to the kitchen subsequently bring a banana to Bob")
token1 = doc[4]
print(token1.similarity(nlp("then")[0]))