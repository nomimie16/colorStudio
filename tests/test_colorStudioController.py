import pytest
from unittest.mock import MagicMock
from colorStudioController import (
    CSController,
    CSLightController,
    CSAEController,
    CSColorWheelController,
    CSSaturationController
)

# ----------------------------------------------------------------------------------
# CSController
# ----------------------------------------------------------------------------------
class TestCSController:
    def test_init_attrbutes(self):
        #création de faux objects
        fake_root = MagicMock()
        fake_scene = MagicMock()
        fake_widget = MagicMock()
        fake_cwidget = MagicMock()
        
        #création du controller
        controler = CSController(
            root = fake_root,
            scene = fake_scene,
            widget = fake_widget,
            controlledWidget = fake_cwidget
        )
        
        #vérifie la sortie/création
        assert controler._sceneRoot is fake_root
        assert controler._scene is fake_scene
        assert controler._widget is fake_widget
        assert controler._controlledWidget is fake_cwidget
    
    def test_event_ne_fait_rien(self):#à changer par la suite??
        ctrl = CSController()
        resultat = ctrl._event(None, ("donothing",))
        assert resultat is None
        
# ----------------------------------------------------------------------------------
# CSLightController
# ----------------------------------------------------------------------------------
class TestCSLightController:
    
    #création de "fixture" pour déclarer une seule fois les objets
    @pytest.fixture
    def fake_root(self):
        root = MagicMock()
        root.render.return_value = MagicMock(name="fake_img")
        return root
    
    @pytest.fixture
    def fake_light(self):
        light = MagicMock()
        light._name = "TitreLumière"
        return light
        
    @pytest.fixture
    def fake_widget(self):
        widget = [MagicMock(), MagicMock()]
        return widget
    
    @pytest.fixture
    def fake_cwidget(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_cwController(self):
        return MagicMock()
    
    @pytest.fixture
    def controller(self, fake_root, fake_light, fake_widget, fake_cwidget, fake_cwController):
        return CSLightController(
            root = fake_root,
            light = fake_light,
            widget = fake_widget,
            cwidget = fake_cwidget,
            cwController = fake_cwController
        )

    #init
    def test_init_attributes(self, fake_root, fake_light, fake_widget, fake_cwidget, fake_cwController, controller):
        #vérifie la sortie/création
        assert controller._sceneRoot is fake_root
        assert controller._scene is fake_light
        assert controller._widget is fake_widget
        assert controller._controlledWidget is fake_cwidget
        assert controller._colorWheelController is fake_cwController
    
    #eventType == 0
    def test_event_type_setImageIdx(self, fake_root, fake_light, fake_widget, controller):
        #création de faux objects
        fake_img = MagicMock()
        
        #quand on appelle render ça va retourner fake_img
        fake_root.render.return_value = fake_img

        #on simule mouvement du slider
        #(0 l'évent de type slider et 36 sa position)
        #None paramètre que _event attend mais n'utilise pas
        controller._event(None, (0,36))

        #vérifications
        fake_light.setImageIdx.assert_called_once_with(36)
        fake_root.render.assert_called_once()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)

    #eventType == 2
    def test_event_type_setWindowTitle(self, fake_light, fake_widget, fake_cwController, controller):
        #on simule mouvement du slider
        #event à 2 pour changer la lumière active du color wheel
        controller._event(None, (2,))
        
        #vérif titre de la fen a été maj
        fake_cwController._controlledWidget.setWindowTitle.assert_called_once_with(
            "Color Wheel::TitreLumière"
        )
        
        #vérif maj du controller vers la bonne lumière
        assert fake_cwController._scene is fake_light


    #eventType == -1
    def test_event_type_setExposure(self, fake_root, fake_light, fake_widget, controller):
        #on simulle eventType == 1 : augmenter l'exposition de 1.5
        controller._event(None, (1,1.5))
        fake_light.setExposure.assert_called_once_with(1.5)
        
        #on remet à 0 le mock pour tester eventType == -1
        fake_light.setExposure.reset_mock()
        
        #on simulle eventType == 1 : augmenter l'exposition de 1.5
        controller._event(None, (-1, 0.5))
        fake_light.setExposure.assert_called_once_with(0.5)

# ----------------------------------------------------------------------------------
# CSAEController
# ----------------------------------------------------------------------------------
class TestCSAEController:
    
    #création de fixture éviter la création multiple du même objet
    @pytest.fixture
    def fake_root(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_postprocess(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_widget(self):
        return [MagicMock(), MagicMock()]
    
    @pytest.fixture
    def fake_cwidget(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_img(self):
        return MagicMock()
    
    @pytest.fixture
    def controller(self, fake_root, fake_postprocess, fake_widget, fake_cwidget):
        return CSAEController(
            root = fake_root,
            postprocess = fake_postprocess,
            widget = fake_widget,
            cwidget = fake_cwidget
        )
    
    #init
    def test_init_attributes(self, fake_root, fake_postprocess, fake_widget, fake_cwidget, controller):
        assert controller._sceneRoot is fake_root
        assert controller._scene is fake_postprocess
        assert controller._widget is fake_widget
        assert controller._controlledWidget is fake_cwidget

    #eventType == 0
    def test_setOnOff(self, fake_root, fake_postprocess, fake_widget, fake_img, controller):
        #quand on appelle le render ça va appeler fake_img
        fake_root.render.return_value = fake_img
        
        #on simule du descrease de l'exposure
        # 0=eventType et 1=valeur passée à setOnOff
        #None paramètre que _event attend mais n'utilise pas
        controller._event(None, (0,1))
        
        #vérifications
        fake_postprocess.setOnOff.assert_called_once_with(1)
        fake_root.render.assert_called_once()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)#vérifier que la méthode ai été exécuté

    #eventType == 1 or -1
    def test_setExposure(self, fake_root, fake_postprocess, fake_widget, fake_img, controller):
        #quand on appelle le render ça va appeler fake_img
        fake_root.render.return_value = fake_img
        
        #on simiule le changement d'exposure pour eventType = 1
        #augmentation par 1.5
        controller._event(None, (1,1.5))
        
        #vérifications
        fake_postprocess.setExposure.assert_called_once_with(1.5)
        fake_root.render.assert_called_once_with()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)
        
        # on remet les mocks à zéro pour tester -1
        fake_postprocess.setExposure.reset_mock()
        fake_root.render.reset_mock()
        for w in fake_widget:
            w._update.reset_mock()
        
        #on simule le changement d'exposure pour eventType = -1
        controller._event(None, (-1,0.5))
        
        #vérification
        fake_postprocess.setExposure.assert_called_once_with(0.5)
        fake_root.render.assert_called_once_with()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)

# ----------------------------------------------------------------------------------
# CSColorWheelController
# ----------------------------------------------------------------------------------
class TestCSColorWheelController:
    
    #création de fixture éviter la création multiple du même objet
    @pytest.fixture
    def fake_root(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_light(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_widget(self):
        return [MagicMock(), MagicMock()]
    
    @pytest.fixture
    def fake_cwidget(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_img(self):
        return MagicMock()
    
    @pytest.fixture
    def controller(self, fake_root, fake_light, fake_widget, fake_cwidget):
        return CSColorWheelController(
            root = fake_root,
            light = fake_light,
            widget = fake_widget,
            cwidget = fake_cwidget
        )
    
    #init
    def test_init_attributes(self, fake_root, fake_light, fake_widget, fake_cwidget, controller):
        assert controller._sceneRoot is fake_root
        assert controller._scene is fake_light
        assert controller._widget is fake_widget
        assert controller._controlledWidget is fake_cwidget

    #test de la condition si la scene est None
    def test_sceneIsNoneThenNothing(self, fake_root, fake_widget):
        #création d'un controlleur SANS SCENE
        ctrlWithoutScene = CSColorWheelController(
            root = fake_root,
            light = None,
            widget = fake_widget
        )
        
        #metttre la scene à None
        ctrlWithoutScene._scene = None

        #on simule le changement de couleur
        ctrlWithoutScene._event(None, (0, (255,0,0)))
        
        #le render ne doit pas être appelé
        fake_root.render.assert_not_called()

    #eventType == 0
    def test_setColor(self, fake_root, fake_light, fake_widget, fake_img, controller):
        #quand on appelle render ça va retourner fake_img
        fake_root.render.return_value = fake_img
        
        #on simule le changement de couleur
        controller._event(None, (0,(255,0,0)))
        
        #vérifications
        fake_light.setColor.assert_called_once_with((255,0,0))
        fake_root.render.assert_called_once_with()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)

# ----------------------------------------------------------------------------------
# CSSaturationController
# ----------------------------------------------------------------------------------
class TestCSSaturationController:
    
    @pytest.fixture
    def fake_root(self):
        return MagicMock()
        
    @pytest.fixture
    def fake_postprocess(self):
        return MagicMock()
        
    @pytest.fixture
    def fake_widget(self):
        return [MagicMock(), MagicMock()]
        
    @pytest.fixture
    def fake_cwidget(self):
        return MagicMock()
    
    @pytest.fixture
    def fake_img(self):
        return MagicMock()
    
    @pytest.fixture
    def controller(self, fake_root, fake_postprocess, fake_widget, fake_cwidget):
        return CSSaturationController(
            root = fake_root,
            postprocess = fake_postprocess,
            widget = fake_widget,
            cwidget = fake_cwidget
        )
    
    #init
    def test_init_attrbutes(self, fake_root, fake_postprocess, fake_widget, fake_cwidget, controller):
        assert controller._sceneRoot is fake_root
        assert controller._scene is fake_postprocess
        assert controller._widget is fake_widget
        assert controller._controlledWidget is fake_cwidget

    #eventType = 0 
    def test_setLinearSaturation(self, fake_root, fake_postprocess, fake_img, fake_widget, controller):
        #quand on appelle render ça va retourner fake_img
        fake_root.render.return_value = fake_img
        
        #on simule l'ajout de saturation linéaire
        #(0 l'évent et 2 la valeur de la saturation)
        controller._event(None, (0,2))
        
        #vérifications
        fake_postprocess.setLinearSaturation.assert_called_once_with(2)
        fake_root.render.assert_called_once_with()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)
        
    #eventType == 1
    def test_setGammaSaturation(self, fake_root, fake_postprocess, fake_img, fake_widget, controller):
        #quand on appelle render ça va retourner fake_img
        fake_root.render.return_value = fake_img
        
        #on simule l'ajout de saturation gamme
        #(1 l'évent et 2 la valeur de la saturation)
        controller._event(None, (1,3))
        
        #vérifications
        fake_postprocess.setGammaSaturation.assert_called_once_with(3)
        fake_root.render.assert_called_once_with()
        for w in fake_widget:
            w._update.assert_called_once_with(fake_img)