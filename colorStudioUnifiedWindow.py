# -*- coding: utf-8 -*-
"""
Color Studio - Fenêtre Unifiée
----------------------------------
"""
import skimage

from PyQt6.QtWidgets import (
    QWidget, QMainWindow, QLabel, QPushButton,
    QVBoxLayout, QHBoxLayout, QSlider, QSplitter,
    QGroupBox, QFrame, QScrollArea, QSizePolicy,
    QFileDialog
)
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt, QSize

import colorStudioModel
import colorStudioWidget
import colorStudioController


# ----------------------------------------
#  Palette & constantes de style
# ----------------------------------------
DARK_BG      = "#f0f8ff"
PANEL_BG     = "#e6f3ff"
CARD_BG      = "#ffffff"
ACCENT       = "#2196f3"
ACCENT_SOFT  = "#64b5f6"
TEXT_PRIMARY = "#1a237e"
TEXT_MUTED   = "#5c6bc0"
BORDER       = "#bbdefb"
SLIDER_TRACK = "#e3f2fd"
SLIDER_THUMB = "#2196f3"
BTN_BG       = "#e3f2fd"
BTN_HOVER    = "#1976d2"
BTN_PRESS    = "#0d47a1"

STYLESHEET = f"""
/* -- Fenêtre & Fonds -- */
QMainWindow, QWidget {{
    background-color: {DARK_BG};
    color: {TEXT_PRIMARY};
    font-family: "Consolas", "Courier New", monospace;
    font-size: 12px;
}}

/* -- GroupBox -- */
QGroupBox {{
    border: 1px solid {BORDER};
    border-radius: 8px;
    margin-top: 18px;
    padding: 8px 6px 6px 6px;
    background-color: {PANEL_BG};
    font-weight: bold;
    font-size: 11px;
    letter-spacing: 1px;
    color: {TEXT_MUTED};
    text-transform: uppercase;
}}
QGroupBox::title {{
    subcontrol-origin: margin;
    left: 12px;
    padding: 0 6px;
    color: {ACCENT};
    font-size: 10px;
    letter-spacing: 2px;
}}

/* -- Boutons -- */
QPushButton {{
    background-color: {BTN_BG};
    color: {TEXT_PRIMARY};
    border: 1px solid {BORDER};
    border-radius: 5px;
    padding: 5px 10px;
    font-family: "Consolas", monospace;
    font-size: 11px;
    letter-spacing: 1px;
}}
QPushButton:hover {{
    background-color: {BTN_HOVER};
    border-color: {BTN_HOVER};
    color: #ffffff;
}}
QPushButton:pressed {{
    background-color: {BTN_PRESS};
}}
QPushButton:checked {{
    background-color: {ACCENT};
    border-color: {ACCENT};
    color: #ffffff;
}}
QPushButton#iconBtn {{
    padding: 4px 8px;
    font-size: 14px;
    min-width: 28px;
    max-width: 28px;
}}
QPushButton#smallBtn {{
    min-width: 28px;
    max-width: 28px;
    font-weight: bold;
    font-size: 14px;
    padding: 2px 0;
}}

/* -- Labels -- */
QLabel {{
    color: {TEXT_PRIMARY};
    background: transparent;
}}
QLabel#sectionTitle {{
    color: {TEXT_MUTED};
    font-size: 10px;
    letter-spacing: 2px;
    text-transform: uppercase;
}}
QLabel#valueLabel {{
    color: {ACCENT};
    font-size: 13px;
    font-weight: bold;
    min-width: 52px;
    qproperty-alignment: AlignCenter;
}}

/* -- Sliders -- */
QSlider::groove:horizontal {{
    background: {SLIDER_TRACK};
    height: 4px;
    border-radius: 2px;
}}
QSlider::sub-page:horizontal {{
    background: {ACCENT};
    height: 4px;
    border-radius: 2px;
}}
QSlider::handle:horizontal {{
    background: {SLIDER_THUMB};
    border: 2px solid {DARK_BG};
    width: 14px;
    height: 14px;
    margin: -5px 0;
    border-radius: 7px;
}}
QSlider::handle:horizontal:hover {{
    background: #ff6b80;
    width: 16px;
    height: 16px;
    margin: -6px 0;
    border-radius: 8px;
}}

/* -- Séparateurs -- */
QFrame#hline {{
    color: {BORDER};
    max-height: 1px;
    background: {BORDER};
}}

/* -- ScrollArea -- */
QScrollArea {{
    border: none;
    background: transparent;
}}
QScrollBar:vertical {{
    background: {PANEL_BG};
    width: 6px;
    border-radius: 3px;
}}
QScrollBar::handle:vertical {{
    background: {BORDER};
    border-radius: 3px;
    min-height: 20px;
}}
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
    height: 0;
}}

/* -- Splitter -- */
QSplitter::handle {{
    background: {BORDER};
    width: 2px;
    height: 2px;
}}
"""


# ---------------------------------------------
#  Widget d'encart "render" avec aspect-ratio
# ---------------------------------------------
class AspectRatioContainer(QWidget):
    """Enveloppe le widget de rendu pour conserver le ratio 16:9."""

    def __init__(self, child_widget, parent=None):
        super().__init__(parent)
        self._child = child_widget
        child_widget.setParent(self)
        self.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding)

    def resizeEvent(self, event):
        w = self.width()
        h = self.height()
        # Calcul du rectangle 16:9 centré
        target_ratio = 16 / 9
        if w / h > target_ratio:
            new_w = int(h * target_ratio)
            new_h = h
        else:
            new_w = w
            new_h = int(w / target_ratio)
        x = (w - new_w) // 2
        y = (h - new_h) // 2
        self._child.setGeometry(x, y, new_w, new_h)
        super().resizeEvent(event)


# ----------------------------
#  Helpers de mise en page
# ----------------------------
def hline():
    f = QFrame()
    f.setObjectName("hline")
    f.setFrameShape(QFrame.Shape.HLine)
    return f


def label(text, obj_name=None):
    l = QLabel(text)
    if obj_name:
        l.setObjectName(obj_name)
    return l


def value_label(text="+0.00"):
    l = QLabel(text)
    l.setObjectName("valueLabel")
    return l


def small_btn(text):
    b = QPushButton(text)
    b.setObjectName("smallBtn")
    return b


# -----------------------
#  Fenêtre principale
# -----------------------
class ColorStudioUnifiedWindow(QMainWindow):
    """Fenêtre principale unifiée pour Color Studio"""

    def __init__(self, lightsScene):
        super().__init__()
        self.lightsScene = lightsScene
        self.setWindowTitle("COLOR STUDIO")
        self.setGeometry(80, 80, 1600, 950)
        self.setMinimumSize(1200, 720)
        self._current_light_idx = 0

        self._loadIcons()
        self._setupUI()
        self._setupControllers()
        self._updateRender()

    # -- Icônes --
    def _loadIcons(self):
        try:
            p = './images/others/'
            self.uiLoadIMG  = QIcon(p + 'uiLoad.png')
            self.uiSaveIMG  = QIcon(p + 'uiSave.png')
            self.uiAEonIMG  = QIcon(p + 'uiAEon.png')
            self.uiAEoffIMG = QIcon(p + 'uiAEoff.png')
        except Exception:
            self.uiLoadIMG = self.uiSaveIMG = self.uiAEonIMG = self.uiAEoffIMG = QIcon()

    # -- Construction de l'UI --
    def _setupUI(self):
        self.setStyleSheet(STYLESHEET)

        root = QWidget()
        self.setCentralWidget(root)

        # Splitter principal : gauche | centre | droite
        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.setHandleWidth(2)

        splitter.addWidget(self._buildLeftPanel())
        splitter.addWidget(self._buildCenterPanel())
        splitter.addWidget(self._buildRightPanel())

        # Proportions initiales (pixels) : 300 | stretch | 320
        splitter.setSizes([300, 9999, 320])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setStretchFactor(2, 0)

        root_layout = QHBoxLayout(root)
        root_layout.setContentsMargins(8, 8, 8, 8)
        root_layout.addWidget(splitter)

    # -- Panneau gauche --
    def _buildLeftPanel(self):
        panel = QWidget()
        panel.setMaximumWidth(320)
        panel.setMinimumWidth(240)
        outer = QVBoxLayout(panel)
        outer.setContentsMargins(0, 0, 4, 0)
        outer.setSpacing(6)

        # Load / Save
        file_group = QGroupBox("Fichier")
        fl = QHBoxLayout(file_group)
        fl.setSpacing(6)
        load_btn = QPushButton("  Charger")
        load_btn.setIcon(self.uiLoadIMG)
        load_btn.setIconSize(QSize(18, 18))
        load_btn.clicked.connect(self._loadScene)
        save_btn = QPushButton("  Sauvegarder")
        save_btn.setIcon(self.uiSaveIMG)
        save_btn.setIconSize(QSize(18, 18))
        save_btn.clicked.connect(self._saveScene)
        fl.addWidget(load_btn)
        fl.addWidget(save_btn)
        outer.addWidget(file_group)

        # Scroll pour les lumières (si beaucoup de lumières)
        lights_group = QGroupBox("Lumières")
        lights_outer = QVBoxLayout(lights_group)
        lights_outer.setContentsMargins(4, 4, 4, 4)
        lights_outer.setSpacing(4)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        scroll_content = QWidget()
        self._lights_scroll_layout = QVBoxLayout(scroll_content)
        self._lights_scroll_layout.setSpacing(6)
        self._lights_scroll_layout.setContentsMargins(2, 2, 2, 2)
        scroll.setWidget(scroll_content)
        lights_outer.addWidget(scroll)
        outer.addWidget(lights_group, 1)

        # Post-traitement
        post_group = QGroupBox("Post-traitement")
        pl = QVBoxLayout(post_group)
        pl.setSpacing(8)

        # AE
        self._ae_control = self._buildAEControl()
        pl.addWidget(self._ae_control)
        pl.addWidget(hline())

        # Saturation
        self._sat_control = self._buildSatControl()
        pl.addWidget(self._sat_control)

        outer.addWidget(post_group)
        return panel

    def _buildLightControl(self, light, index):
        """Construire le widget de contrôle pour une lumière."""
        card = QGroupBox(f"LIGHT {index}  ·  {light._name}")
        cl = QVBoxLayout(card)
        cl.setSpacing(6)
        cl.setContentsMargins(8, 10, 8, 8)

        # Exposition
        exp_row = QHBoxLayout()
        exp_row.setSpacing(4)
        dec = small_btn("−")
        inc = small_btn("+")
        exp_lbl = value_label(f"{light._exposure:+.2f}")
        self._exposure_labels.append(exp_lbl)

        color_btn = QPushButton("Couleur")
        color_btn.setFixedHeight(26)
        self._color_buttons.append(color_btn)
        self._updateColorButton(index)

        dec.clicked.connect(lambda _, i=index: self._changeExposure(i, -0.2))
        inc.clicked.connect(lambda _, i=index: self._changeExposure(i, +0.2))
        color_btn.clicked.connect(lambda _, i=index: self._selectColor(i))

        exp_row.addWidget(label("EV", "sectionTitle"))
        exp_row.addWidget(dec)
        exp_row.addWidget(exp_lbl)
        exp_row.addWidget(inc)
        exp_row.addStretch()
        exp_row.addWidget(color_btn)
        cl.addLayout(exp_row)

        # Slider de position
        pos_row = QVBoxLayout()
        pos_row.setSpacing(2)
        pos_row.addWidget(label("POSITION", "sectionTitle"))

        pos_slider = QSlider(Qt.Orientation.Horizontal)
        pos_slider.setMinimum(0)
        pos_slider.setMaximum(max(0, light._maxIdx - 1))
        pos_slider.setValue(light._imageIdx)
        pos_slider.valueChanged.connect(lambda v, i=index: self._changePosition(i, v))
        self._position_sliders.append(pos_slider)
        pos_row.addWidget(pos_slider)
        cl.addLayout(pos_row)

        return card

    def _buildAEControl(self):
        w = QWidget()
        l = QHBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(6)

        l.addWidget(label("AUTO EXP", "sectionTitle"))

        self._ae_btn = QPushButton("ON")
        self._ae_btn.setCheckable(True)
        self._ae_btn.setChecked(True)
        self._ae_btn.setFixedWidth(44)
        self._ae_btn.clicked.connect(self._toggleAE)
        l.addWidget(self._ae_btn)

        dec = small_btn("−")
        self._ae_exp_label = value_label("+0.00")
        inc = small_btn("+")
        dec.clicked.connect(lambda: self._changeAEExposure(-0.2))
        inc.clicked.connect(lambda: self._changeAEExposure(+0.2))

        l.addWidget(dec)
        l.addWidget(self._ae_exp_label)
        l.addWidget(inc)
        l.addStretch()
        return w

    def _buildSatControl(self):
        w = QWidget()
        l = QVBoxLayout(w)
        l.setContentsMargins(0, 0, 0, 0)
        l.setSpacing(6)

        for attr, title in [("_linear", "Saturation Linéaire"), ("_gamma", "Saturation Gamma")]:
            row = QHBoxLayout()
            row.setSpacing(6)
            row.addWidget(label(title, "sectionTitle"))
            slider = QSlider(Qt.Orientation.Horizontal)
            slider.setMinimum(-100)
            slider.setMaximum(100)
            slider.setValue(0)
            lbl = value_label("0")
            row.addWidget(slider)
            row.addWidget(lbl)
            l.addLayout(row)

            if attr == "_linear":
                self._linear_slider, self._linear_label = slider, lbl
                slider.valueChanged.connect(self._changeLinearSaturation)
            else:
                self._gamma_slider, self._gamma_label = slider, lbl
                slider.valueChanged.connect(self._changeGammaSaturation)

        return w

    # -- Panneau central --
    def _buildCenterPanel(self):
        panel = QWidget()
        ol = QVBoxLayout(panel)
        ol.setContentsMargins(4, 0, 4, 0)
        ol.setSpacing(4)

        # Titre de section
        header = QLabel("RENDU")
        header.setObjectName("sectionTitle")
        header.setAlignment(Qt.AlignmentFlag.AlignLeft)
        ol.addWidget(header)

        # Widget de rendu dans son conteneur aspect-ratio
        self._render_widget = colorStudioWidget.CSDisplayWidget(None)
        self._render_widget.setSizePolicy(
            QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Expanding
        )
        container = AspectRatioContainer(self._render_widget)
        ol.addWidget(container, 1)

        return panel

    # -- Panneau droit --
    def _buildRightPanel(self):
        panel = QWidget()
        panel.setMaximumWidth(340)
        panel.setMinimumWidth(260)
        ol = QVBoxLayout(panel)
        ol.setContentsMargins(4, 0, 0, 0)
        ol.setSpacing(6)

        # Color Wheel
        cw_group = QGroupBox("Sélecteur de couleur")
        cw_l = QVBoxLayout(cw_group)
        cw_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._color_wheel_widget = colorStudioWidget.CSDisplayColorWheel(None, 280)
        self._color_wheel_widget.setFixedSize(280, 280)
        cw_l.addWidget(self._color_wheel_widget)
        ol.addWidget(cw_group)

        # Nuage 3D
        c3d_group = QGroupBox("Nuage de points 3D")
        c3d_l = QVBoxLayout(c3d_group)
        c3d_l.setAlignment(Qt.AlignmentFlag.AlignCenter)
        img_small = skimage.transform.rescale(
            self.lightsScene.render(), 0.1,
            anti_aliasing=True, channel_axis=2
        )
        self._color3d_widget = colorStudioWidget.MyWidgetGL(img_small, True)
        self._color3d_widget.setFixedSize(280, 280)
        c3d_l.addWidget(self._color3d_widget)
        ol.addWidget(c3d_group)

        ol.addStretch()
        return panel

    # -- Contrôleurs --
    def _setupControllers(self):
        self._exposure_labels   = []
        self._position_sliders  = []
        self._color_buttons     = []

        # Construire les contrôles lumière maintenant qu'on a les listes
        for i, light in enumerate(self.lightsScene._lights):
            card = self._buildLightControl(light, i)
            self._lights_scroll_layout.addWidget(card)
        self._lights_scroll_layout.addStretch()

        # Color Wheel controller
        self._cw_controller = colorStudioController.CSColorWheelController(
            self.lightsScene, None,
            [self._render_widget, self._color3d_widget],
            self._color_wheel_widget
        )
        self._cw_controller._colorChangeCallback = self._onColorChanged
        self._color_wheel_widget._controller = self._cw_controller

        # Light controllers
        self._light_controllers = []
        for i, light in enumerate(self.lightsScene._lights):
            lc = colorStudioController.CSLightController(
                self.lightsScene, light,
                [self._render_widget, self._color3d_widget]
            )
            lc._colorWheelController = self._cw_controller
            self._light_controllers.append(lc)

        # AE
        ae = colorStudioModel.AE_Ymean(Ytarget=0.5, exposure=0.0)
        self.lightsScene.addPostProcess(ae)
        self._ae_controller = colorStudioController.CSAEController(
            self.lightsScene, ae,
            [self._render_widget, self._color3d_widget]
        )

        # Saturation
        sat = colorStudioModel.Saturation()
        self.lightsScene.addPostProcess(sat)
        self._sat_controller = colorStudioController.CSSaturationController(
            self.lightsScene, sat,
            [self._render_widget, self._color3d_widget]
        )

    # -- Handlers --
    def _changeExposure(self, idx, delta):
        if idx < len(self.lightsScene._lights):
            light = self.lightsScene._lights[idx]
            new_exp = max(-5.0, min(5.0, light._exposure + delta))
            light.setExposure(new_exp)
            self._exposure_labels[idx].setText(f"{new_exp:+.2f}")
            self._updateRender()

    def _changePosition(self, idx, value):
        if idx < len(self.lightsScene._lights):
            self.lightsScene._lights[idx].setImageIdx(value)
            self._updateRender()

    def _selectColor(self, idx):
        if idx < len(self.lightsScene._lights):
            light = self.lightsScene._lights[idx]
            self._cw_controller._scene = light
            self._current_light_idx = idx

    def _onColorChanged(self, light):
        # Find the index of the light that changed
        for i, l in enumerate(self.lightsScene._lights):
            if l == light:
                self._updateColorButton(i)
                break

    def _updateColorButton(self, idx):
        if idx < len(self.lightsScene._lights):
            light = self.lightsScene._lights[idx]
            r, g, b = light._npColorRGB
            color_hex = f"#{int(r*255):02x}{int(g*255):02x}{int(b*255):02x}"
            self._color_buttons[idx].setStyleSheet(
                f"QPushButton {{ background-color: {color_hex}; color: {'white' if (r+g+b)/3 < 0.5 else 'black'}; }}"
            )

    def _saveScene(self):
        filename, _ = QFileDialog.getSaveFileName(
            self, "Sauvegarder la scène", "", "Fichiers XML (*.xml)"
        )
        if filename:
            if not filename.endswith('.xml'):
                filename += '.xml'
            xml_content = self.lightsScene.toXML()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(xml_content)

    def _loadScene(self):
        filename, _ = QFileDialog.getOpenFileName(
            self, "Charger une scène", "", "Fichiers XML (*.xml)"
        )
        if filename:
            self.lightsScene.clear()
            self.lightsScene.fromXML(filename)
            self._rebuildLightControls()

    def _toggleAE(self):
        on = self._ae_btn.isChecked()
        self._ae_btn.setText("ON" if on else "OFF")
        self._ae_controller._scene.setOnOff(on)
        self._updateRender()

    def _changeAEExposure(self, delta):
        current = float(self._ae_exp_label.text())
        new_val = max(-5.0, min(5.0, current + delta))
        self._ae_exp_label.setText(f"{new_val:+.2f}")
        self._ae_controller._scene.setExposure(new_val)
        self._updateRender()

    def _changeLinearSaturation(self, value):
        self._linear_label.setText(str(value))
        self._sat_controller._scene.setLinearSaturation(value)
        self._updateRender()

    def _changeGammaSaturation(self, value):
        self._gamma_label.setText(str(value))
        self._sat_controller._scene.setGammaSaturation(value)
        self._updateRender()

    def _updateRender(self):
        try:
            img = self.lightsScene.render()
            self._render_widget._update(img)
            self._color3d_widget._update(img)
            # Update color buttons when color changes
            for i in range(len(self.lightsScene._lights)):
                self._updateColorButton(i)
        except Exception as e:
            print(f"[ColorStudio] Erreur de rendu : {e}")

    def _rebuildLightControls(self):
        # Clear existing light controls
        while self._lights_scroll_layout.count():
            item = self._lights_scroll_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Reset lists
        self._exposure_labels = []
        self._position_sliders = []
        self._color_buttons = []
        
        # Rebuild light controls
        for i, light in enumerate(self.lightsScene._lights):
            card = self._buildLightControl(light, i)
            self._lights_scroll_layout.addWidget(card)
        self._lights_scroll_layout.addStretch()
        
        # Rebuild controllers
        self._light_controllers = []
        for i, light in enumerate(self.lightsScene._lights):
            lc = colorStudioController.CSLightController(
                self.lightsScene, light,
                [self._render_widget, self._color3d_widget]
            )
            lc._colorWheelController = self._cw_controller
            self._light_controllers.append(lc)
        
        self._updateRender()


# ----------------
#  Factory
# ----------------
def createUnifiedWindow(lightsScene):
    return ColorStudioUnifiedWindow(lightsScene)