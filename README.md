# PoiGraphApi

## Organisation des branches git:
- une branche main qui sert uniquement à porter les versions de release
- une branche develop qui sert à mettre en commun (merger) les branches individuelles de travail. Quand les commits sur develop sont propres et que les fonctionnalités sont opérationnelles, y compris avec le reste du code, cette branche est mergée dans main pour faire un tag de release
- des branches individuelles de travail qui servent à coder et tester les fonctionnalités (ou features). Quand une feature est finalisée, après une code review, les commits de cette branche sont mergées dans develop. Il y aura donc beaucoup de branches individuelles et elles peuvent être considérées comme éphémères.

Important pour éviter les conflits de merge et garder un historique propre : on fait un pull sur develop pour le mettre à jour et après on crée la branche individuelle. Une fois que le travail est finalisé, avant de passer en code review et de merger sur develop, il faut rebaser la branche avec develop de nouveau mis à jour.

## Secrets:
Des secrets Docker ont été mis en place pour protéger les données sensibles comme les identifiants de connexion. Ces secrets sont pris en charge par docker compose qui les passe comme données d'environnement dans les différents containers. Ils sont déclarés uniquement dans le docker-compose.yaml en faisant appel à un répertoire /secrets placé à la racine du projet. 

Ce répertoire /secrets est déclaré dans le .gitignore pour ne pas être commité. Il contient un fichier par secret dont le nom est déclaré dans le docker-compose.yaml. Chaque fichier .txt contient uniquement le secret à protéger sous forme de chaîne de caractère. Le répertoire et tous les fichiers doivent être ajoutés à la racine du projet avant de lancer le docker compose up.

Les secrets sont ensuite accédés dans le code soit à travers les variables d'environnement, soit en scannant les fichiers texte.    

## Description du projet:
