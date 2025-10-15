# PoiGraphApi

## Organisation des branches git:
- une branche main qui sert uniquement à porter les versions de release
- une branche develop qui sert à mettre en commun (merger) les branches individuelles de travail. Quand les commits sur develop sont propres et que les fonctionnalités sont opérationnelles, y compris avec le reste du code, cette branche est mergée dans main pour faire un tag de release
- des branches individuelles de travail qui servent à coder et tester les fonctionnalités (ou features). Quand une feature est finalisée, après une code review, les commits de cette branche sont mergées dans develop. Il y aura donc beaucoup de branches individuelles et elles peuvent être considérées comme éphémères.

Important pour éviter les conflits de merge et garder un historique propre : on fait un pull sur develop pour le mettre à jour et après on crée la branche individuelle. Une fois que le travail est finalisé, avant de passer en code review et de merger sur develop, il faut rebaser la branche avec develop de nouveau mis à jour.

## Description du projet:
