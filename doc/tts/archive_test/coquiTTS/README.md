
`pip install TTS`  
Pour tester l'installation : `tts`, liste des modèles : `tts --list_models` 
 
Met a disposition un outil pratique : `tts-server`, nous pouvons alors tester différent model avec par exemple la commande `tts-server --model_name "tts_models/en/ljspeech/fast_pitch"` qui va nous permettre de tester le modèle sur un serveur local.  
![screen1](./img/screen1.png)  

Après en avoir tester plusieurs, certains modèles comme le `speedy-speech` ou le `fast_pitch` semblent être les plus rapide tout en étant compréhensible.  
Sur le serveur de démo, nous avons des temps d'inférence entre 0.5 secondes et un peu moins d'1 sconde pour les modèles de ce type.
![screen2](./img/screen2.png)  
Les autres modèle ont environ 2 seconde et quelques de temps de calcul    
