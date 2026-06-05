# ColorStudio

ColorStudio est un outil de compositing et de rendu d'images de synthèse dévelopée en PyQt6.

[![Version](https://img.shields.io/badge/version-0.13.0-blue.svg)](https://github.com/nomimie16/skyrift)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Documentation](https://img.shields.io/badge/docs-online-brightgreen.svg)](https://nomimie16.github.io/skyrift)


## Description
L'application ColorStudio est un outil de compositing et de rendu d'images de synthèse dévelopée en PyQt6. Le logiciel permet de fusionner plusieurs images issues de rendus distincts afin de produire une image finale cohérente que l’on peut ajuster comme on veut.


## Installation

- Téléchargement de l'exécutable
  - Rendez vous sur le dépôt GitHub officiel : [ColorStudio Github]((https://github.com/nomimie16/colorStudio))
  - Dans la section "Releases", à droite, cliquez sur la dernière version téléchargeable.
  - Téléchargez l'exécutable correspondant à votre système.

## Lancement de l'application
- Lancement depuis l'executable
  - Double-cliquez sur l'exécutable téléchargé pour lancer l'application.

- Lancement depuis un terminal de commande :
    - Ouvrez un terminal de commande (cmd, PowerShell, Terminal, etc.)
    - executez ```python src/colorStudioApp.py```

## Dépendances

* [PyQt6](https://www.riverbankcomputing.com/software/pyqt/) :  Framework d'interface graphique pour le développement de l'application.

* [ModernGL](https://moderngl.readthedocs.io/) : Bibliothèque de rendu OpenGL pour la visualisation du nuage de points 3D.

* [Pytest](https://docs.pytest.org/en/stable/) : Framework de tests automatisés.

* [mkdocs](https://www.mkdocs.org/) : Générateur de documentation statique utilisé pour créer la documentation du projet.


## Structure du projet 

```
src/
├── colorStudioApp.py       → Point d'entrée
├── colorStudioModel.py     → Modèle (Images, Light, Scene)
├── colorStudioUtils.py     → Utilitaires (IO, transformations)
├── controllers/            → Contrôleurs (logique métier)
└── ui/                     → Interface graphique
    ├── builders/           → Construction UI
    └── widget/             → Widgets OpenGL

```

## Documentation

Pour visualiser la documentation détaillée, rendez vous sur [https://nomimie16.github.io/colorStudio/](https://nomimie16.github.io/colorStudio/).

* Documentation utilisateur : installation, interface, FAQ, etc.
* Documentation technique : Structure, développement, architecture.

## Auteurs

* [CHAGOT Manon](https://github.com/Manuki17)
* [LIGNIER Noémie](https://github.com/nomimie16) 
* [CHATELAIN Lilou](https://github.com/liiloouu16) 
