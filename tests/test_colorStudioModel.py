import pytest
import numpy as np
from unittest.mock import MagicMock

from sympy import resultant
from colorStudioModel import(
    PostProcess,
    Images,
    Scene,
    Light,
    AE_Ymean,
    Saturation,
    PPClip
)

# ----------------------------------------------------------------------------------
#  POST PROCESS
# ----------------------------------------------------------------------------------
class TestPostProcess:
    def test_postProcess_retourne_img (self):
        #création d'un objet post process
        pp = PostProcess()
        
        #création d'une fausse image (10 lignes, 10 col, 3 "couleurs" RGB)
        img = np.ones((10, 10, 5))
        
        #Appel de la méthode que l'on veut tester
        resultat = pp.postProcess(img)
        
        #vérification
        assert resultat is img  

# ----------------------------------------------------------------------------------
#  LIGHT
# ----------------------------------------------------------------------------------
class TestLight:
    def test_init_valeur(self):
        
        light1 = Light()
        light1 = Light(name="Soleil")
        assert light1._name == "Soleil"
        
        light = Light()
        assert "Light" in light._name
        assert np.array_equal(light._npColorRGB, [1.0,1.0,1.0])
        assert light._exposure == 0
        assert light._imageIdx == 0
        assert light._maxIdx == 0
        assert light._ImagesArray is None
        assert light._needUpdate is False
        assert light._firstUpdate is True
        assert light._currentImage is None
    
    def test_setImagesArray(self):
        #création d'un objet Light
        light = Light()
        
        fake_images = MagicMock()
        fake_images.len.return_value = 10
        
        #on appel la procédure
        light.setImagesArray(fake_images)
        
        #vérifications
        assert light._ImagesArray is fake_images
        assert light._maxIdx == 10
        
    def test_clear(self):
        light = Light()
        fake_images = MagicMock()
        light._ImagesArray = fake_images
        
        light.clear()
        
        fake_images.clear.assert_called_once()

    def test_setExposure(self):
        light = Light()
        light.setExposure(2.5)
        assert light._exposure == 2.5
        assert light._needUpdate is True
        
    def test_setColor(self):
        light = Light()
        nouv_couleur = np.array([0.5,0.2,0.8])
        light.setColor(nouv_couleur)
        assert np.array_equal(light._npColorRGB, nouv_couleur)
        assert light._needUpdate is True
        
    def test_setImageIdx(self):
        light = Light()
        light.setImageIdx(5)
        assert light._imageIdx == 5
        assert light._needUpdate is True
    
    def test_render(self):
        light = Light()
        #on créer une fausse image blanche
        fake_img = np.ones((4,4,3))
        #on créer un faux tableau d'image
        fake_images = MagicMock()
        fake_images._images = [fake_img]
        light._ImagesArray = fake_images
        resultat = light.render()
        #vérification des résultats
        assert resultat.shape == (4,4,3)
        assert light._firstUpdate is False
        assert light._needUpdate is False

# ----------------------------------------------------------------------------------
#  SCENE
# ----------------------------------------------------------------------------------
class TestScene:
    def test_init_valeur(self):
        scene = Scene()
        assert scene._lights == []
        assert scene._postProcesses == []
        assert scene._hdr is False
        
    def test_init_hdr(self):
        scene = Scene(hdr=True)
        assert scene._hdr == True
        
    def test_addLight(self):
        scene = Scene()
        fake_light = MagicMock()
        
        #essaie de la fonction
        scene.addLight(fake_light)
        
        #vérifie si la fake light, la light de test, a bien été ajoutée
        assert fake_light in scene._lights
        #vérifie si une seule a bien été ajoutée
        assert len(scene._lights) == 1
        
    def test_addPostProcess(self):
        scene = Scene()
        fake_postProcess = MagicMock()
        
        #essaie de la fonction
        scene.addPostProcess(fake_postProcess)
        
        #vérification si le postProcess de test a bien été ajouté
        assert fake_postProcess in scene._postProcesses
        #vérifie si un seul postProcess a bien été ajouté
        assert len(scene._postProcesses) == 1

    def test_clear(self):
        #préparation de la scene test
        scene = Scene()
        scene.addLight(MagicMock())
        scene.addPostProcess(MagicMock())

        #vérification s'il y a bien des éléments
        assert len(scene._lights) == 1
        assert len(scene._postProcesses) == 1
        
        #appel de la fonction clear
        scene.clear()
        
        #vérification du fonctionnement de la fonction
        #vérifie donc si les listes sont vides
        assert scene._lights == []
        assert scene._postProcesses == []

    def test_getLightByName_trouve(self):
        scene = Scene()
        fake_light = MagicMock()
        fake_light._name = "Soleil"
        scene.addLight(fake_light)
        
        resultat = scene.getLightByName("Soleil")
        assert resultat is fake_light
        
    def test_getLightByName_nonTrouve(self):
        scene = Scene()
        fake_light = MagicMock()
        fake_light._name = "Soleil"
        scene.addLight(fake_light)
        
        resultat = scene.getLightByName("Lampadaire")
        #censé ne rien trouver donc ne rien retourner
        assert resultat is None

    def test_render_une_seule_lumiere(self):
        scene = Scene()
        fake_light = MagicMock()
        
        #on lui dit quoi retourner quand on appelle render 
        fake_light.render.return_value = np.ones((4,4,3)) *0.5
        scene.addLight(fake_light)
        
        #forme de l'image nécessaire pour np.zeros
        fake_light._ImagesArray._images = [np.zeros((4,4,3))]
        
        resultat = scene.render()

        assert resultat.shape == (4,4,3)
        assert np.allclose(resultat, 0.5)
        
    def test_render_deux_lumieres(self):
        scene = Scene()
        
        #préparation de la première lumière
        fake_light1 = MagicMock()
        fake_light1.render.return_value = np.ones((4,4,3)) * 0.4
        
        #préparation de la première lumière
        fake_light2 = MagicMock()
        fake_light2.render.return_value = np.ones((4,4,3)) * 0.3
        
        scene.addLight(fake_light1)
        scene.addLight(fake_light2)
        
        resultat = scene.render()
        
        # 0.4+0.3 = 0.7
        assert np.allclose(resultat, 0.7)

    def test_render_hdr(self):
        scene = Scene(hdr = True)
        fake_light = MagicMock()
        fake_light.render.return_value = np.ones((4,4,3)) *2.0
        fake_light._ImagesArray._images = [np.zeros((4,4,3))]
        scene.addLight(fake_light)
        resultat = scene.render()
        assert np.allclose(resultat, 2.0)
        
# ----------------------------------------------------------------------------------
#  POST PROCESS : SATURATION -VIBRANCE 
# ----------------------------------------------------------------------------------
class TestSaturation:
    def test_init_attributes(self):
        sat = Saturation()
        assert sat._linearSaturation == 0
        assert sat._gammaSaturation == 0
        assert sat._saturationRange == 1.0
        
    def test_setLinearSaturation(self):
        sat = Saturation()
        sat.setLinearSaturation(50)
        assert sat._linearSaturation == 50
        
    def test_setGammaSaturation(self):
        sat = Saturation()
        sat.setGammaSaturation(25)
        assert sat._gammaSaturation == 25
        
    def test_postProcess_saturation_zero(self):
        sat = Saturation()
        img = np.ones((4, 4, 3)) * 0.5
        resultat = sat.postProcess(img)
        # rien ne doit changer
        assert np.allclose(resultat, img)
