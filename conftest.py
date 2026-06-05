import sys
import os

# dossier racine
root = os.path.dirname(__file__)

# on ajoute tous les dossiers nécessaires
sys.path.insert(0, os.path.join(root, "src"))
sys.path.insert(0, os.path.join(root, "src", "controllers"))
sys.path.insert(0, os.path.join(root, "src", "ui", "builders"))
sys.path.insert(0, os.path.join(root, "src", "ui", "widget"))