## Synopsis
Vous trouverez dans le fichier `feureur.py` le code src du bot pour Discord.

Sa fonction est de surveiller les salons et de réagir lorsqu'il détecte la présence du q-word dans un message.

Il existe une liste de mots authorisés contenant la séquence de lettre "q-u-o-i" tels que carquois, sequoia, etc. ; si vous les utilisez, le bot vous signalera qu'il vous tient à l'œil...

Vous avez également la possibilité de vous protéger en contrant le bot avec "antifeur", il vous en témoignera parfois son désarrois.

## Fichiers
Ce projet contient plusieurs fichiers et utilise la plateforme Heroku qui permet aux développeurs de créer, déployer et gérer des applications dans le cloud. Si vous n'utilisez pas Heroku, vous pouvez ignorer les fichiers `requirements.txt` et `Procfile`.
- `.gitignore`
- `Procfile` : indique à Heroku comment exécuter l'application.
- `README.md`
- `feureur.py` : code src de l'application.
- `requirements.txt` : liste toutes les dépendances Python nécessaires pour l'application.
- `todolist.txt`

## Lexique
- guild : serveur discord
- channel : salon