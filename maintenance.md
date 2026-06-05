---
title: Maintenance et support
summary: Guide de maintenance du projet
---
---

## Dépannage

### La fenêtre d'image ne s'affiche pas
- Vérifier le chemin XML
- Vérifier que les images existent
- Vérifier les permissions d'accès

### Performance lente
- Réduire la résolution des images
- Diminuer le nombre d'images chargées
- Vérifier la RAM disponible

---

## Tests
``` 
python -m pytest tests/ 
```
- Tests unitaires pour les fonctions de traitement d'images

---

## Mise à jour PyQt6/OpenGL

``` 
pip install --upgrade PyQt6 PyOpenGL ModernGL
```
- Vérifier la compatibilité des versions

---

### Utilisation de Git

* **Bonnes pratiques :**

    * Créer une branche pour chaque fonctionnalité ou correction
    * Utiliser des messages de commit clairs
    * Tester le jeu avant chaque push
    * Exemple de message de commit :
    ```fix: correction bug déplacement dragon```

* **Ce projet respecte la [convention de commit](https://www.conventionalcommits.org/en/v1.0.0/) :**

    * ```fix:``` corrige un bug dans le code
    * ```feat:``` introduit une nouvelle fonctionnalité dans le code
    * ```docs:``` ajoute un changement au sein de la documentation
    * ```refactor:``` spécifie un changement dans le code qui ne corrige pas de bug et n'ajoute pas de nouvelle fonctionnalité
    * ```tests:``` ajoute des tests manquants ou des corrections de tests

---

## Publier des mises à jour

### Générer un exécutable

Un exécutable peut être généré à l’aide d’un outil tel que [PyInstaller](https://pyinstaller.org/en/stable/).

Exemple :
```
pyinstaller main.py --onefile
```

### Publier une nouvelle version

* **Étapes recommandées :**

    * Mettre à jour le code
    * Tester le jeu
    * Mettre à jour le changelog
    * Créer un tag Git
    * Publier la version
