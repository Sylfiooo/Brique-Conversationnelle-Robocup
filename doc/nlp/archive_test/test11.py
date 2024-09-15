import re

def trouver_nombre_complexe(chaine):
    # Utiliser une expression régulière pour trouver les nombres complexes dans la chaîne
    regex_nombre_complexe = re.compile(r'\b(?:zero|one|two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|and)\b', re.IGNORECASE)
    
    matches = regex_nombre_complexe.findall(chaine)
    
    # Si on a trouvé des nombres complexes
    if matches:
        nombre_complex = ' '.join(matches)
        return nombre_complex
    else:
        return None

# Exemple d'utilisation
chaine_test = "I go to Paris where i seen three thousand two hundred and fifty beers, then i go to London and i live at five PM"
nombre_complex = trouver_nombre_complexe(chaine_test)

if nombre_complex:
    print(f"Le nombre complexe trouvé dans la chaîne est '{nombre_complex}'.")
else:
    print("Aucun nombre complexe trouvé dans la chaîne.")