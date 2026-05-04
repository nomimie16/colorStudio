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
# EasyGUI to PyQt6.QFileDialog
# ----------------------------------------------------------------------------------
# Requires Python >= 3.13
# Tested on Python 3.13.12  
# ----------------------------------------------------------------------------------
# version0.0
# ----------------------------------------------------------------------------------
# Qt window

# import(s)
# ----------------------------------------------------------------------------------
import sys

from PyQt6.QtWidgets import QApplication, QFileDialog

import colorStudioModel
import colorStudioWidget
import colorStudioUIBuilder

# ----------------------------------------------------------------------------------		
print("ColorStudio - Rémi Cozot - 2019")
print("-------------------------------")
screenX, screenY = colorStudioWidget.getScreenSize()
print("screen resolution: ",screenX,"x",screenY)
colorStudioUIBuilder.CSUIAllBuilder.setTemplate(screenX,screenY)

# Qt init
app = QApplication.instance() 
if not app:  app = QApplication(sys.argv)

# select input file name
defaultFilename = "./xml-2019-6-7-22-47-1.xml" 
inputFilename, _ = QFileDialog.getOpenFileName(None, "Select light-setup file", "", "XML files (*.xml)")
print("ColorStudio: inuput file>",inputFilename)

if inputFilename == None: 
    inputFilename= defaultFilename
    print("ColorStudio: inuput file>",inputFilename)


# scene object
lightsScene = colorStudioModel.Scene()
# load scene from xml
lightsScene.fromXML(inputFilename,colorStudioUIBuilder.CSUIBuilder.template['scale'])
# print scene
lightsScene.print()

# build GUI according to scene
ui = colorStudioUIBuilder.CSUIAllBuilder(lightsScene)

# run app for event management
app.exec()

