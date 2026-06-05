# -*- coding: utf-8 -*-
"""
Color Studio - Rémi Cozot 2019
----------------------------------
new version of 
Color Studio - Rémi Cozot 2019
"""
# ----------------------------------------------------------------------------------
# main changes
# ----------------------------------------------------------------------------------
# GUI : PyQt5 to PyQt6
# import(s)
# ----------------------------------------------------------------------------------
import sys

from PyQt6.QtWidgets import QApplication, QFileDialog

import colorStudioUnifiedWindow as colorStudioUnifiedWindow



# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
class CSUIBuilder:
        # class attributes
        uiLoadIMG  	= None
        uiSaveIMG  	= None
        uiAEonIMG  	= None
        uiAEoffIMG 	= None
        uiDEIMG 	= None
        uiIEIMG 	=  None
        uiCCIMG 	=  None

        template1920x1080 = { 'scale': 0.5 ,                     \
            'uiRenderWidget_pos' : (480,30),                    \
            'uiRenderWidget_size' : (int(1920/2),int(1080/2)),  \
            # color3D widget
            'uiColor3DWidget_pos' : (1440,30),                  \
            'uiColor3DWidget_size' : (480,480),                 \
            # color wheel widget
            'uiColorWheelWidget_pos' : (1440,540),              \
            'uiColorWheelWidget_size' : (480,480),              \
            # menu/control widget
            'uiControlWidget_pos' : (0,30),                     \
            'uiControlWidget_size' : (480,0)}

        template3000x200 = { 'scale': 1,                        \
            'uiRenderWidget_pos' : (int(480*1.25),60),          \
            'uiRenderWidget_size' : (int(1920),int(1080)),      \
            # color3D widget
            'uiColor3DWidget_pos' : (3000-480,60),              \
            'uiColor3DWidget_size' : (480,480),                 \
            # color wheel widget
            'uiColorWheelWidget_pos' : (3000-480,540+60),       \
            'uiColorWheelWidget_size' : (480,480),              \
            # menu/control widget
            'uiControlWidget_pos' : (0,60),                     \
            'uiControlWidget_size' : (480,0)}

        template = template1920x1080

        # class method
        def setTemplate(widthSceen,heightScreen):
            if widthSceen == 3000 : CSUIBuilder.template = CSUIBuilder.template3000x200

        # constructor
        def __init__(self):
            pass

        # class method
        def uiLoadIcon(pathUIimg=None):
            if pathUIimg==None: pathUIimg = './images/others/'
            # window with buttons
            CSUIBuilder.uiLoadIMG  	= QIcon(pathUIimg+'uiLoad.png')
            CSUIBuilder.uiSaveIMG  	= QIcon(pathUIimg+'uiSave.png')
            CSUIBuilder.uiAEonIMG  	= QIcon(pathUIimg+'uiAEon.png')
            CSUIBuilder.uiAEoffIMG 	= QIcon(pathUIimg+'uiAEoff.png')
            CSUIBuilder.uiDEIMG 	=  QIcon(pathUIimg+'uiLight_F_DE.png')
            CSUIBuilder.uiIEIMG 	=  QIcon(pathUIimg+'uiLight_F_IE.png')
            CSUIBuilder.uiCCIMG 	=  QIcon(pathUIimg+'uiLight_F_CC.png')
# ----------------------------------------------------------------------------------

# ----------------------------------------------------------------------------------
class CSUIAllBuilder(CSUIBuilder):
    def __init__(self, lightsScene, use_unified=True):
        # Nouvelle interface unifiée
        self._unifiedWindow = colorStudioUnifiedWindow.ColorStudioUnifiedWindow(lightsScene)
        self._unifiedWindow.show()

# ----------------------------------------------------------------------------------
# ----------------------------------------------------------------------------------
