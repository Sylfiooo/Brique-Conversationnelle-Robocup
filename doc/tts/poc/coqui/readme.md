# Installation technique
Si jamais probleme de cython ou de pyyaml pendant le pip install TTS  

Aller voir https://github.com/yaml/pyyaml/issues/724 notamment la commande `pip install "cython<3.0.0" && pip install --no-build-isolation pyyaml==6.0`  

Il faut apparement une version supérieur a 3.7 également. => https://www.itsupportwale.com/blog/how-to-upgrade-to-python-3-7-on-ubuntu-18-10/  

Possiblement des problèmes de version de setuptools => mettre a jour pip `python3 -m pip install -U pip`


Les modèles téléchargés se trouvent par défaut dans `.local/share/tts`