---
title: Annexes
summary: Informations techniques et utiles lors du développement du projet
---
---

## Glossaire

| Terme                   | Définition                                 |   
|-------------------------|--------------------------------------------|
| **Compositing**         | Fusion de plusieurs images en une seule    |   
| **EV (Exposure Value)** | Unité de mesure de luminosité              | 
| **Nuage de points**     | Représentation 3D des couleurs             | 
| **XML**                 | Format de sérialisation des configurations |  

---

## Conventions de code

- Noms de classes : PascalCase (Light, Scene)
- Noms de fonctions : snake_case (load_images)
- Variables privées : _prefixe_underscore
- Commentaires : Docstrings pour chaque classe/fonction

---

## Commandes utiles

- Lancer l'application : `python src/colorStudioApp.py`
- Installer les dépendances : `pip install -r requirements.txt`
- Lancer les tests : `python -m pytest tests/`

---

## Ressources

- [PyQt6 Documentation](https://doc.qt.io/qt-6/)
- [ModernGL](https://moderngl.readthedocs.io/)
- [scikit-image](https://scikit-image.org/)

---

## Historique

- **2019** : Version initiale (Rémi Cozot)
- **2026** : Migration Pygame → PyQt6, ajout nuage 3D

---

## Gestion de versions et bonnes pratiques

### **Git – Documentation officielle**  
* [https://git-scm.com/doc](https://git-scm.com/doc)  
*  Outil de gestion de versions utilisé pour le projet.

### **Conventional Commits**  
* [https://www.conventionalcommits.org/en/v1.0.0/](https://www.conventionalcommits.org/en/v1.0.0/)
* Convention utilisée pour la rédaction des messages de commit.

---

## Tests 

### **Pytest – Documentation officielle**  
* [https://docs.pytest.org/en/stable/](https://docs.pytest.org/en/stable/)
* Framework de tests utilisé pour les tests unitaires du projet.


---

## Documentation

### **Markdown – Guide de syntaxe**  
* [https://www.markdownguide.org/](https://www.markdownguide.org/)
* Langage de balisage utilisé pour la rédaction de la documentation.

### **MkDocs – Documentation officielle**  
* [https://www.mkdocs.org/]([https://www.mkdocs.org/])
* Générateur de site de documentation utilisé pour le projet.

### **Shadcn - Thème pour la documentation**
* [https://github.com/asiffer/mkdocs-shadcn?tab=readme-ov-file](https://github.com/asiffer/mkdocs-shadcn?tab=readme-ov-file)
* Thème mkdocs pour un design élégant

---