# Module de traitement automatique du langage naturel (NLP)

### Navigation
[HOME](https://github.com/Sylfiooo/Brique-Conversationnelle-Robocup)  
[STT](../stt/)  
[TTS](../tts/) 

**Auteurs** :
* Vincent BUNIAZET
* Lucas COUDRAIS
* Alexis THOMAS



- [Module de traitement automatique du langage naturel (NLP)](#module-de-traitement-automatique-du-langage-naturel-nlp)
    - [Navigation](#navigation)
  - [Description](#description)
  - [Etat de l'art](#etat-de-lart)
    - [SpaCy](#spacy)
      - [Introduction](#introduction)
      - [Caractéristiques principales](#caractéristiques-principales)
      - [Utilisations Courantes](#utilisations-courantes)
      - [Exemple d'utilisation](#exemple-dutilisation)
      - [Conclusion](#conclusion)
    - [Transformers (Hugging Face)](#transformers-hugging-face)
      - [Introduction](#introduction-1)
      - [Caractéristiques principales](#caractéristiques-principales-1)
      - [Utilisations courantes](#utilisations-courantes-1)
      - [Exemple d'utilisation](#exemple-dutilisation-1)
      - [Conclusion](#conclusion-1)
    - [NLTK (Natural Language Toolkit)](#nltk-natural-language-toolkit)
      - [Introduction](#introduction-2)
      - [Caractéristiques principales](#caractéristiques-principales-2)
      - [Utilisations courantes](#utilisations-courantes-2)
      - [Exemple d'utilisation](#exemple-dutilisation-2)
      - [Conclusion](#conclusion-2)
    - [Polyglot](#polyglot)
      - [Introduction](#introduction-3)
      - [Caractéristiques principales](#caractéristiques-principales-3)
      - [Utilisations courantes](#utilisations-courantes-3)
      - [Exemple d'utilisation](#exemple-dutilisation-3)
      - [Conclusion](#conclusion-3)
  - [Choix de la librairie](#choix-de-la-librairie)
  - [Utilisation du module](#utilisation-du-module)
    - [ROS-less](#ros-less)
      - [Commandes à lancer](#commandes-à-lancer)
      - [Fonctionnement des fonctions](#fonctionnement-des-fonctions)
        - [sentenceSplitter (sentence : string, debug = False : bool)](#sentencesplitter-sentence--string-debug--false--bool)
          - [Exemple](#exemple)
        - [orderFormatter (sentence : string, debug = False : bool)](#orderformatter-sentence--string-debug--false--bool)
          - [Exemple](#exemple-1)
        - [sentenceCreator(objectFormatted : \[dict\], debug = False : bool)](#sentencecreatorobjectformatted--dict-debug--false--bool)
          - [Exemple](#exemple-2)
    - [ROS2](#ros2)
      - [Commandes à lancer](#commandes-à-lancer-1)
      - [Utilisation des services](#utilisation-des-services)
        - [Sentence Splitter : /sentence\_splitter](#sentence-splitter--sentence_splitter)
        - [Order Formatter : /order\_formatter](#order-formatter--order_formatter)
        - [Sentence Creator : /sentence\_creator](#sentence-creator--sentence_creator)

## Description

Ce module va proposer plusieurs services ROS2 permettant l'interaction avec du texte composé d'ordres, et va identifier les éléments essentiels à la compréhension des instructions fournies.

## Etat de l'art

Il existe en Python de nombreuses librairies utilisables pour faire du NLP, celles-ci ont cependant toutes des avantages et des inconvénients.

### SpaCy

#### Introduction
spaCy est une bibliothèque open-source pour le traitement du langage naturel (NLP) en Python. Elle est conçue pour être rapide, efficace et facile à utiliser. spaCy offre des fonctionnalités puissantes pour le prétraitement du texte, l'analyse syntaxique, l'analyse d'entités nommées, la reconnaissance d'entités, la lemmatisation, le marquage de discours et d'autres tâches liées au traitement du langage naturel.

#### Caractéristiques principales

- **Traitement rapide** : spaCy est réputé pour sa rapidité d'exécution. Il est écrit en Cython, ce qui le rend performant et adapté à une utilisation dans des applications en temps réel.
-  **Modèles pré-entraînés** : Elle  fournit des modèles pré-entraînés pour plusieurs langues, facilitant ainsi le démarrage rapide de projets sans avoir besoin d'entraîner un modèle à partir de zéro.
-  **Analyse syntaxique** : La bibliothèque offre une analyse syntaxique robuste, permettant de comprendre la structure grammaticale d'une phrase, y compris la détection des dépendances entre les mots.
-  **Reconnaissance d'Entités Nommées (NER)** :  spaCy excelle dans la reconnaissance et l'étiquetage d'entités nommées telles que les personnes, les lieux, les organisations, etc. 
-  **Lemmatisation** : Il fournit des fonctionnalités de lemmatisation qui simplifient les mots à leur forme de base.
-  **Intégration avec d'autres bibliothèques** : spaCy s'intègre facilement avec d'autres bibliothèques populaires de l'écosystème Python, telles que scikit-learn et TensorFlow.
-  **Support multi-langues** : En plus du support pour plusieurs langues, spaCy propose des modèles entraînés pour des langues non-occidentales.

#### Utilisations Courantes

- **Analyse de texte** : Pour extraire des informations importantes d'un texte, comme les entités nommées, les relations, etc.
- **Traitement Automatique du Langage Naturel (TALN)** : Pour créer des applications de traitement du langage naturel, telles que les chatbots, les systèmes de recommandation, etc.
- **Extraction d'informations** : Pour extraire des informations structurées à partir de documents texte.
- **Classification de texte** : Pour classer les textes en catégories prédéfinies.

#### Exemple d'utilisation

```python
!pip install spacy
!pip install fr_core_news_sm

import spacy
​
nlp = spacy.load("fr_core_news_sm")
​
text = "Apple a été créée en 1976 par Steve Wozniak, Steve Jobs et Ron Wayne."
​
# Traite le texte
doc = nlp(text)
​
# Itère sur les entités prédites
for ent in doc.ents:
    # Affiche le texte de l'entité et son label
    print(ent.text, ent.label_)
```

#### Conclusion

spaCy est devenu un choix populaire parmi les chercheurs et les développeurs en NLP en raison de sa facilité d'utilisation, de ses performances élevées et de sa polyvalence. Son développement actif et sa communauté active en font une bibliothèque de premier choix pour ceux qui travaillent dans le domaine du traitement du langage naturel avec Python.

### Transformers (Hugging Face)

#### Introduction

Les Transformers, développés par Hugging Face, sont une bibliothèque open-source qui a révolutionné le traitement du langage naturel (NLP) et d'autres domaines de l'apprentissage automatique. Cette bibliothèque se concentre sur l'utilisation et le déploiement facile de modèles transformer pré-entraînés, offrant ainsi une puissante boîte à outils pour les tâches de traitement du langage naturel et bien au-delà.

#### Caractéristiques principales

- **Modèles pré-entrainés** : Hugging Face propose un large éventail de modèles transformer pré-entraînés, y compris BERT, GPT, RoBERTa, et bien d'autres, qui ont établi de nouveaux standards de performance dans diverses tâches de NLP.
- **Facilité d'utilisation** : Transformers simplifie grandement l'utilisation de modèles transformer complexes. Il offre une interface simple pour charger, entraîner et évaluer ces modèles.
- **Compatibilité multi-tâches** :  La bibliothèque est polyvalente et peut être utilisée pour une variété de tâches telles que la classification de texte, la génération de texte, la traduction automatique, la résumé automatique, etc.
- **Hub de modèles** :   Hugging Face propose un hub de modèles (Model Hub) qui permet aux utilisateurs de partager, découvrir et utiliser des modèles pré-entraînés facilement.
- **Fine-Tuning** : Les modèles transformer de Hugging Face peuvent être fine-tunés sur des tâches spécifiques avec un effort minimal, ce qui les rend adaptés à une variété d'applications personnalisées.
- **Intégration avec d'autres bibliothèques** : Transformers s'intègre bien avec d'autres bibliothèques populaires comme PyTorch et TensorFlow.

#### Utilisations courantes
- **Traitement du Langage Naturel (NLP)** : Les Transformers sont largement utilisés pour des tâches telles que la classification de texte, l'analyse de sentiments, la génération de texte, et la compréhension de texte.
- **Traduction automatique** : Ils sont efficaces pour la traduction automatique entre différentes langues.
- **Résumé automatique** : Les modèles transformer peuvent générer des résumés automatiques de textes longs.
- **Reconnaissance d'entités** : Ils sont utiles dans la reconnaissance d'entités nommées et d'autres tâches d'extraction d'informations.

#### Exemple d'utilisation

```python
!pip install transformers

from transformers import pipeline

classifier = pipeline("sentiment-analysis")
classifier(
    [
        "I've been waiting for a HuggingFace course my whole life.",
        "I hate this so much!",
    ]
)
```

#### Conclusion
Transformers de Hugging Face a joué un rôle crucial dans l'avancement rapide du traitement du langage naturel. En offrant une gamme complète de modèles liées au NLP et une facilité d'utilisation remarquable, cette bibliothèque a eu un impact significatif sur la manière dont les chercheurs et les praticiens abordent les problèmes liés au langage naturel. Avec une communauté active et un support continu, Transformers continue de jouer un rôle central dans l'évolution du domaine de l'apprentissage automatique appliqué au langage.

### NLTK (Natural Language Toolkit)

#### Introduction
Le Natural Language Toolkit (NLTK) est une bibliothèque Python populaire et complète pour le traitement du langage naturel (NLP). Conçu pour être éducatif, extensible et fonctionnel, NLTK offre une gamme d'outils et de ressources pour la manipulation et l'analyse de données textuelles, ce qui en fait un choix prisé dans la communauté du traitement du langage naturel.

#### Caractéristiques principales
- **Outils de prétraitement textuel** : NLTK propose une variété d'outils pour le prétraitement du texte, y compris la tokenisation, la lemmatisation, la suppression de stopwords, etc...
- **Collections de données linguistiques** : La bibliothèque comprend des corpus et des ressources lexicales couvrant un large éventail de langues, ce qui facilite la recherche et le développement dans des contextes multilingues.
- **Algorithme d'analyse syntaxique** : NLTK inclut un analyseur syntaxique qui permet d'explorer la structure grammaticale des phrases et de détecter les relations entre les mots.
- **Méthodes de classification de texte** : La librairie offre des outils pour la classification de texte y compris des implémentations de classificateurs tels que Naive Bayes.
- **Intégration de modèles statistiques** : La bibliothèque intègre des modèles statistiques pour des tâches spécifiques telles que la reconnaissance d'entités nommées (NER) et l'étiquetage de parties du discours (POS tagging).
- **Support pour le traitement des langues** : NLTK fournit des fonctionnalités pour le traitement de plusieurs langues, ce qui en fait un outil polyvalent pour des applications globales.

#### Utilisations courantes
- **Éducation et apprentissage** :  NLTK est largement utilisé dans les programmes éducatifs et les cours liés au NLP en raison de sa documentation complète et de son caractère éducatif.
- **Recherche académique** : Il est utilisé dans la recherche universitaire pour explorer des questions liées au traitement du langage naturel.
- **Prototypage rapide** : NLTK est souvent utilisé pour prototyper rapidement des idées et des algorithmes dans le domaine du NLP.
- **Développement d'applications NLP** : La bibliothèque est utilisée pour développer des applications NLP telles que des systèmes de chatbot simples, des analyseurs de sentiment, etc.

#### Exemple d'utilisation

```python
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
text = 'In this tutorial, I\'m learning NLTK. It is an interesting platform.'
stop_words = set(stopwords.words('english'))
words = word_tokenize(text)
new_sentence = []
for word in words:
    if word not in stop_words:
  	new_sentence.append(word)
print(new_sentence)
```

#### Conclusion
NLTK, avec sa longue histoire et son engagement envers l'éducation, continue d'être un choix solide pour les débutants dans le domaine du traitement du langage naturel. Bien qu'il puisse être considéré comme moins spécialisé que certaines bibliothèques plus récentes, NLTK reste pertinent pour des tâches éducatives, de recherche et de prototypage, en particulier pour ceux qui souhaitent comprendre en profondeur les mécanismes internes du NLP.

### Polyglot

#### Introduction
Polyglot est une bibliothèque Python dédiée au traitement du langage naturel (NLP) qui se distingue par son support multilingue étendu. Conçue pour être polyvalente et accessible, Polyglot offre une gamme d'outils pour l'analyse de texte dans différentes langues, facilitant ainsi le traitement de données multilingues.

#### Caractéristiques principales
- **Support multilingue** : Polyglot se distingue par son vaste support pour plusieurs langues, permettant aux utilisateurs de travailler avec des données textuelles dans différentes langues sans nécessiter des configurations spécifiques.
- **Extraction d'entitées nommées** : La bibliothèque propose des fonctionnalités avancées d'extraction d'entités nommées, permettant la reconnaissance d'entités telles que les personnes, les lieux et les organisations.
- **Analyse syntaxique** : Polyglot offre une analyse syntaxique pour comprendre la structure grammaticale des phrases et les relations entre les mots.
- **Reconnaissance de la langue** : La bibliothèque peut automatiquement détecter la langue d'un texte, facilitant le traitement de documents contenant plusieurs langues.
- **Intégration de vecteurs de mots** : Polyglot peut intégrer des vecteurs de mots pré-entraînés pour améliorer la représentation sémantique des mots dans différentes langues.
- **Classification de texte** : Elle propose des outils pour la classification de texte, aidant à catégoriser les documents en fonction de catégories prédéfinies.

#### Utilisations courantes
- **Analyse multilingue** : Polyglot est couramment utilisé dans des contextes où le traitement de texte multilingue est essentiel, tels que la surveillance des médias sociaux à l'échelle mondiale.
- **Recherche en sciences sociales** : La bibliothèque est utilisée pour analyser des corpus multilingues dans des études sociolinguistiques et d'autres domaines connexes.
- **Traitement de données web** : Polyglot est utile pour extraire des informations multilingues à partir de pages web et d'autres sources en ligne.
- **Projets d'analyse de sentiments globaux** : En raison de son support multilingue, Polyglot est employé dans des projets d'analyse de sentiments couvrant plusieurs langues.

#### Exemple d'utilisation
```python
!pip install polyglot
!pip install pyicu 
!pip install Morfessor
!pip install pycld2 

%%bash
polyglot download ner2.en

%%bash
polyglot download pos2.en

%%bash
polyglot download sentiment2.en

from polyglot.detect import Detector
spanish_text = u"""¡Hola ! Mi nombre es Ana. Tengo veinticinco años. Vivo en Miami, Florida"""
detector = Detector(spanish_text)
print(detector.language)
```

#### Conclusion
Polyglot se distingue par son support multilingue étendu, faisant d'elle une bibliothèque précieuse pour des applications qui nécessitent le traitement de texte dans différentes langues. Son intégration de fonctionnalités avancées d'analyse syntaxique et d'extraction d'entitées nommées en fait une option attrayante pour ceux qui cherchent à explorer et à comprendre la diversité linguistique à travers le traitement du langage naturel.

## Choix de la librairie
Pour ses nombreux avantages, nous nous tournons vers la librairie spaCy :
- Rapidité et performances élevées
- Facilité d'utilisation
- Support actif
- Documentation complète
- Adaptation à divers domaines

## Utilisation du module

Le module peut être utilisé sous deux formes : En tant que noeud ROS2 en proposant des services, ou sous la forme d'une simple librairie Python à référencer.

### ROS-less

#### Commandes à lancer

```cmd
pip install -r requirements.txt # Installation des dépendances
```

#### Fonctionnement des fonctions

##### sentenceSplitter (sentence : string, debug = False : bool)
La fonction prend un texte en entrée et va découper l'entrée en sous-phrases, en fonction des verbes et des mots qui pourraient séparer les différentes parties.

###### Exemple
```python
sentenceSplitter("go into the kitchen and into the bathroom, bring two bananas, a potato and three tacos to Bob and to Cassy and catch me a beer")
>>> ['go into the kitchen and into the bathroom', 'bring two bananas , a potato and three tacos to Bob and to Cassy', 'catch me a beer']
```

##### orderFormatter (sentence : string, debug = False : bool)
La fonction va prendre un ordre sous forme de chaine en entrée, et va retourner en objet formaté permettant de distinguer les éléments importants de l'ordre.

###### Exemple
```python
orderFormatter("bring two bananas and three tacos into the kitchen")
>>> {'action' : 'bring', 'params' : [{'name':'bananas', 'number':'2'}, {'name':'tacos', 'number':'3'}], 'into': ['kitchen']}
```

##### sentenceCreator(objectFormatted : [dict], debug = False : bool)

La fonction va prendre un ordre formaté et va retourner une question de confirmation -permettant d'interroger l'utilisateur sur la bonne compréhension de la phrase.

###### Exemple
```python
sentenceCreator([{'action': 'put', 'params': [{'name': 'knife'}], 'on': ['table']}, {'action': 'return', 'in': ['bathroom']}])
>>> "so I need to put the knife on the table and then I have to return in the bathroom ?"
```

### ROS2

#### Commandes à lancer

Allez dans ws_NLP et lancez ces commandes :

```cmd
pip install -r requirements.txt # Installation des dépendances
colcon build #Build des packages
```

Ouvrez un nouveau terminal dans ce workspace et lancer ces commandes :
```cmd
source install/setup.bash #CPasSourcé
ros2 run nlp nlp
```

Les services sont disponibles.

#### Utilisation des services

##### Sentence Splitter : /sentence_splitter
Ce service permet de transformer une phrase composée d'ordres en un tableau de sous-phrases, découpées en fonction de l'analyse syntaxique de celle-ci.

**Request** :
- string sentence (Ex: ``'go into the kitchen and into the bathroom , bring two bananas , a potato and three tacos to Bob and to Cassy and catch me a beer'``)

**Response** :
- string[] subphrases (Ex : ``['go into the kitchen and into the bathroom', 'bring two bananas , a potato and three tacos to Bob and to Cassy', 'catch me a beer']``)

##### Order Formatter : /order_formatter
Ce service permet de transformer une phrase sous la forme d'un ordre en un objet JSON stringifié décrivant les éléments essentiels de l'ordre (verbe, préposition, personne...)

**Request** : 
- string sentence (Ex :``'bring two bananas , a potato and three tacos to Bob and to Cassy'``)

**Response** :
- string object_formatted (Ex : ``"{'action': 'bring', 'params': [{'name': 'bananas', 'number': 2}, {'name': 'potato', 'number': 1}, {'name': 'tacos', 'number': 3}], 'to': ['Bob', 'Cassy']}"``)

##### Sentence Creator : /sentence_creator
Ce service permet de créer une question de confirmation permettant d'interroger l'utilisateur sur la bonne compréhension de la phrase à partir d'un tableau rempli d'objets JSON d'ordres formatés stringifiés.

**Request** :
- string[] objects_formatted (Ex : ``["{'action': 'go', 'into': ['kitchen', 'bathroom']}"," {'action': 'bring', 'params': [{'name': 'bananas', 'number': 2}, {'name': 'potato', 'number': 1}, {'name': 'tacos', 'number': 3}], 'to': ['Bob', 'Cassy']}", "{'action': 'catch', 'person': ['me'], 'params': [{'name': 'beer', 'number': 1}]}"]``)
  
**Response** :
- string sentence (Ex : ``so I have to go into the kitchen and the bathroom and I need to bring 2 bananas, 1 potato and 3 tacos to Bob and Cassy and after that I need to catch you 1 beer ?``)