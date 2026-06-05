import pytest
from unittest.mock import MagicMock
from unittest.mock import patch
from colorStudioUIBuilder import (
    CSUIBuilder,
    CSUIAllBuilder
)

# ----------------------------------------------------------------------------------
# CSUIBuilder
# ----------------------------------------------------------------------------------
class TestCSUIBuilder:
    #vérifier que le template a les bonnes clés
    def test_template_1920x1080_contient_bonnes_cles(self):
        cles_attendues = [
            'scale',
            'uiRenderWidget_pos',
            'uiRenderWidget_size',
            'uiColor3DWidget_pos',
            'uiColor3DWidget_size',
            'uiColorWheelWidget_pos',
            'uiColorWheelWidget_size',
            'uiControlWidget_pos',
            'uiControlWidget_size'
        ]
        for cle in cles_attendues:
            assert cle in CSUIBuilder.template1920x1080

    #vérifier que le template a les bonnes clés
    def test_template_3000x200_contient_bonnes_cles(self):
        cles_attendues = [
            'scale',
            'uiRenderWidget_pos',
            'uiRenderWidget_size',
            'uiColor3DWidget_pos',
            'uiColor3DWidget_size',
            'uiColorWheelWidget_pos',
            'uiColorWheelWidget_size',
            'uiControlWidget_pos',
            'uiControlWidget_size',
        ]
        for cle in cles_attendues:
            assert cle in CSUIBuilder.template3000x200
    
    #test de la méthode set template            
    def test_setTemplate3000(self):
        CSUIBuilder.setTemplate(3000,200)
        assert CSUIBuilder.template is CSUIBuilder.template3000x200
        
    #test de la méthode set template (2ème)           
    def test_setTemplate1920(self):
        #remettre le template par défaut
        CSUIBuilder.template = CSUIBuilder.template1920x1080
        CSUIBuilder.setTemplate(1920, 108041)
        #on vérifie que ça correspond bien
        assert CSUIBuilder.template is CSUIBuilder.template1920x1080
        
    def test_uiLoadIcon(self):
        with patch("colorStudioUIBuilder.QIcon") as fake_qicon:
            fake_qicon.return_value = MagicMock()

            #on appelle la fonction
            CSUIBuilder.uiLoadIcon()
            
            #on vérifie les résultats de la fonction
            #on vérifie que les boutons ne sont pas nul
            assert CSUIBuilder.uiLoadIMG is not None
            assert CSUIBuilder.uiSaveIMG is not None
            assert CSUIBuilder.uiAEonIMG is not None
            assert CSUIBuilder.uiAEoffIMG is not None
            assert CSUIBuilder.uiDEIMG is not None
            assert CSUIBuilder.uiIEIMG is not None
            assert CSUIBuilder.uiCCIMG is not None
        
        
# Pas de test pour la suite : car pas de calcul, pas d'algorithme, pas de logique métier, que du placement d'icon, par "testable". 