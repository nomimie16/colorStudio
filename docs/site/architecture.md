---
title: Architecture
summary: Présentation de l'architecture du projet
---
---


---

## Structure et organisation du code

Le projet respecte les principes suivants :

* Lisibilité et **clarté** du code
* **Réutilisabilité** des composants
* Facilité de **maintenance**


## Architecture du projet

L’arborescence suivante représente l’organisation générale du projet.  
Elle pourra évoluer en fonction des besoins et de l’avancement du développement.

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
---

## Utilité des dossiers

- **src/** : Contient tout le code source de l’application
- **controllers/** : Logique métier et gestion des interactions
- **ui/** : Composants d’interface graphique (PyQt6)
    - **builders/** : Fonctions de construction de l’interface
    - **widget/** : Widgets personnalisés (rendu OpenGL)
- **data/** : Contient les fichiers XML et les images utilisées pour les tests et démonstrations
- **docs/** : Documentation du projet (architecture, configuration, maintenance, etc.)
- **tests/** : Tests unitaires pour assurer la qualité du code
- **images/** : Contient les images utilisées pour les tests et démonstrations

---

## Fichiers principaux

- **colorStudioApp.py** : Fichier principal de l’application, initialise l’interface et lance la boucle principale
- **colorStudioModel.py** : Définit les classes principales (Image, Light, Scene) et leurs interactions
- **colorStudioUtils.py** : Fonctions utilitaires pour le chargement/sauvegarde de données, transformations, etc

---

## Classes principales

- **Image** : Gestion d'une série d'images
- **Light** : Propriétés d'une source lumineuse
- **Scene** : Conteneur pour toutes les lumières
- **CSUIWidget** : Widget de rendu OpenGL

---

## Pattern MVC
Model (colorStudioModel) → Controller → View (PyQt6)