# _____________________________ Exporter Blender pour Color Studio _______________________________
# 
# - Dans l'onglet "Édition" de Blender, sélectionnez "Paramètres"
# - Allez dans "Add-ons" et faites "Installer depuis les fichiers" en haut à droite de la fenêtre
# - Sélectionnez le fichier blenderColorStudioExporter.py
# - Activez l'extension
# - Redémarrez Blender
# - Vous pourrez voir apparaître "Color Studio" dans la barre latérale
# - Vous pouvez configurer l'export et le lancer
# - Toutes les images ainsi que le fichier XML seront générés dans le répertoire spécifié
# ________________________________________________________________________________________________

bl_info = {
    "name": "Color Studio Exporter",
    "author": "SAE Maintenance Logicielle",
    "version": (1, 0),
    "blender": (2, 80, 0),
    "location": "View3D > Sidebar > Color Studio",
    "description": "Export light sequences for Color Studio compositing",
    "warning": "",
    "doc_url": "",
    "category": "Import-Export",
}

import bpy
import bpy_extras
import os
import xml.etree.ElementTree as ET
from xml.dom import minidom
import mathutils
import math

class ColorStudioExportProperties(bpy.types.PropertyGroup):
    """Propriétés pour l'export Color Studio"""
    
    # Répertoire de sortie
    output_directory: bpy.props.StringProperty(
        name="Output Directory",
        description="Directory to save exported images and XML",
        default="//colorstudio_export/",
        subtype='DIR_PATH'
    )
    
    # Nom de base pour les images
    base_name: bpy.props.StringProperty(
        name="Base Name",
        description="Base name for image sequences",
        default="light01_"
    )
    
    # Nombre d'images par lumière
    image_count: bpy.props.IntProperty(
        name="Image Count",
        description="Number of images to generate per light",
        default=100,
        min=1,
        max=1000
    )
    
    # Format d'image
    image_format: bpy.props.EnumProperty(
        name="Image Format",
        description="Output image format",
        items=[
            ('PNG', 'PNG', 'PNG format'),
            ('JPEG', 'JPEG', 'JPEG format'),
        ],
        default='JPEG'
    )
    
    # Résolution
    resolution_x: bpy.props.IntProperty(
        name="Resolution X",
        description="Output image width",
        default=1920,
        min=1
    )
    
    resolution_y: bpy.props.IntProperty(
        name="Resolution Y", 
        description="Output image height",
        default=1080,
        min=1
    )
    
    # Échantillons de rendu
    render_samples: bpy.props.IntProperty(
        name="Render Samples",
        description="Number of render samples",
        default=128,
        min=1
    )


def get_ext(image_format):
    """Normalise l'extension pour ColorStudio (jpeg -> jpg)"""
    return 'jpg' if image_format == 'JPEG' else 'png'


class COLORSTUDIO_OT_export_lights(bpy.types.Operator):
    """Exporter les séquences de lumières pour Color Studio"""
    bl_idname = "colorstudio.export_lights"
    bl_label = "Export Light Sequences"
    bl_options = {'REGISTER', 'UNDO'}
    
    @classmethod
    def poll(cls, context):
        return context.area and context.area.type == 'VIEW_3D'
    
    def execute(self, context):
        props = context.scene.colorstudio_props
        
        # Vérifier qu'il y a des lumières dans la scène
        lights = [obj for obj in context.scene.objects if obj.type == 'LIGHT']
        if not lights:
            self.report({'ERROR'}, "No lights found in the scene")
            return {'CANCELLED'}
        
        # Créer le répertoire de sortie
        output_path = bpy.path.abspath(props.output_directory)
        os.makedirs(output_path, exist_ok=True)
        
        # Sauvegarder les paramètres actuels du rendu
        original_settings = self.save_render_settings(context.scene)
        
        try:
            # Configurer les paramètres de rendu
            self.setup_render_settings(context.scene, props)
            
            # Exporter chaque lumière
            for light_idx, light in enumerate(lights):
                self.export_light_sequence(context.scene, light, light_idx, props, output_path)
                # Permettre à Blender de traiter les événements entre les lumières
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
            
            # Générer le fichier XML
            xml_file = self.generate_xml_file(lights, props, output_path)
            
            self.report({'INFO'}, f"Export completed: {len(lights)} lights exported to {output_path}")
            self.report({'INFO'}, f"XML file: {xml_file}")
            
        except Exception as e:
            self.report({'ERROR'}, f"Export failed: {str(e)}")
            return {'CANCELLED'}
        
        finally:
            # Restaurer les paramètres originaux
            self.restore_render_settings(context.scene, original_settings)
        
        return {'FINISHED'}
    
    def save_render_settings(self, scene):
        """Sauvegarder les paramètres de rendu actuels"""
        return {
            'resolution_x': scene.render.resolution_x,
            'resolution_y': scene.render.resolution_y,
            'file_format': scene.render.image_settings.file_format,
            'color_mode': scene.render.image_settings.color_mode,
            'quality': scene.render.image_settings.quality,
            'samples': scene.cycles.samples if scene.render.engine == 'CYCLES' else None,
        }
    
    def setup_render_settings(self, scene, props):
        """Configurer les paramètres de rendu pour l'export"""
        scene.render.resolution_x = props.resolution_x
        scene.render.resolution_y = props.resolution_y
        scene.render.image_settings.file_format = props.image_format
        scene.render.image_settings.color_mode = 'RGB'
        
        if props.image_format == 'JPEG':
            scene.render.image_settings.quality = 95
        
        # Configurer les samples pour Cycles
        if scene.render.engine == 'CYCLES':
            scene.cycles.samples = props.render_samples
    
    def restore_render_settings(self, scene, settings):
        """Restaurer les paramètres de rendu originaux"""
        scene.render.resolution_x = settings['resolution_x']
        scene.render.resolution_y = settings['resolution_y']
        scene.render.image_settings.file_format = settings['file_format']
        scene.render.image_settings.color_mode = settings['color_mode']
        scene.render.image_settings.quality = settings['quality']
        
        if settings['samples'] is not None and scene.render.engine == 'CYCLES':
            scene.cycles.samples = settings['samples']
    
    def export_light_sequence(self, scene, light, light_idx, props, output_path):
        """Exporter la séquence d'images pour une lumière"""
        print(f"Exporting light {light_idx}: {light.name}")
        
        ext = get_ext(props.image_format)
        
        # Désactiver toutes les lumières
        for obj in scene.objects:
            if obj.type == 'LIGHT':
                obj.hide_render = True
        
        # Activer seulement la lumière courante
        light.hide_render = False
        
        # Créer une sphère autour de la lumière pour les positions
        light_positions = self.generate_light_positions(light, props.image_count)
        
        # Sauvegarder la position originale
        original_position = light.location.copy()
        original_rotation = light.rotation_euler.copy()
        
        # Rendre chaque position
        for i, pos in enumerate(light_positions):
            # Mettre à jour la position de la lumière
            light.location = pos
            
            # Configurer le nom de fichier de sortie (chemin absolu)
            filename = f"{props.base_name}{i:04d}.{ext}"
            filepath = os.path.join(output_path, filename)
            
            # Rendre l'image
            scene.render.filepath = filepath
            bpy.ops.render.render(write_still=True)
            
            print(f"Rendered {i+1}/{props.image_count}: {filename}")
            
            # Permettre à Blender de traiter les événements pour éviter le freeze
            if i % 5 == 0:  # Tous les 5 rendus
                bpy.ops.wm.redraw_timer(type='DRAW_WIN_SWAP', iterations=1)
        
        # Restaurer la position originale
        light.location = original_position
        light.rotation_euler = original_rotation
    
    def generate_light_positions(self, light, count):
        """Générer les positions de la lumière sur une sphère"""
        positions = []
        
        # Rayon de la sphère (basé sur la distance de la lumière à l'origine)
        radius = light.location.length if light.location.length > 0 else 5.0
        
        for i in range(count):
            # Distribution uniforme sur une sphère
            theta = 2 * math.pi * i / count
            phi = math.acos(1 - 2 * (i + 0.5) / count)
            
            x = radius * math.sin(phi) * math.cos(theta)
            y = radius * math.sin(phi) * math.sin(theta)
            z = radius * math.cos(phi)
            
            positions.append(mathutils.Vector((x, y, z)))
        
        return positions
    
    def generate_xml_file(self, lights, props, output_path):
        """Générer le fichier XML compatible Color Studio"""
        
        ext = get_ext(props.image_format)
        
        # Chemin absolu vers les images (résolu une fois pour toutes)
        abs_base_path = os.path.join(output_path, props.base_name)
        
        # Créer l'élément racine
        lightsetup = ET.Element("LIGHTSETTUP")
        
        # Créer la section LIGHTS
        lights_element = ET.SubElement(lightsetup, "LIGHTS")
        
        # Ajouter chaque lumière
        for light_idx, light in enumerate(lights):
            light_element = ET.SubElement(lights_element, "LIGHT")
            light_element.set("name", f"Light{light_idx}")
            
            # INPUTFILE — chemin absolu pour éviter les problèmes de CWD
            inputfile = ET.SubElement(light_element, "INPUTFILE")
            inputfile.set("ext", f".{ext}")
            inputfile.set("min", "0")
            inputfile.set("max", str(props.image_count - 1))
            inputfile.set("digit", "4")
            inputfile.text = abs_base_path
            
            # IDXPOS (position par défaut)
            idxpos = ET.SubElement(light_element, "IDXPOS")
            idxpos.text = str(props.image_count // 2)  # Position milieu
            
            # EXP (exposition par défaut)
            exp = ET.SubElement(light_element, "EXP")
            exp.text = "0.0"
            
            # COLOR (couleur par défaut blanc)
            color = ET.SubElement(light_element, "COLOR")
            color.set("format", "float")
            
            r = ET.SubElement(color, "R")
            r.text = "1.0"
            g = ET.SubElement(color, "G")
            g.text = "1.0"
            b = ET.SubElement(color, "B")
            b.text = "1.0"
        
        # Ajouter les post-traitements par défaut
        postprocesses = ET.SubElement(lightsetup, "POSTPROCESSES")
        
        # White balance
        wb = ET.SubElement(postprocesses, "POSTPROCESS")
        wb.set("name", "white balance")
        chroma = ET.SubElement(wb, "CHROMA")
        chroma.set("type", "AWB")
        wb_color = ET.SubElement(chroma, "COLOR")
        wb_color.set("format", "float")
        ET.SubElement(wb_color, "R").text = "1.0"
        ET.SubElement(wb_color, "G").text = "1.0"
        ET.SubElement(wb_color, "B").text = "1.0"
        
        # Auto exposure
        ae = ET.SubElement(postprocesses, "POSTPROCESS")
        ae.set("name", "auto exposure")
        luminance = ET.SubElement(ae, "LUMINANCE")
        luminance.set("type", "AE")
        ET.SubElement(luminance, "Y").text = "0.5"
        
        # Gamma
        gamma = ET.SubElement(postprocesses, "POSTPROCESS")
        gamma.set("name", "gamma")
        gamma_lum = ET.SubElement(gamma, "LUMINANCE")
        gamma_lum.set("type", "GAMMA")
        ET.SubElement(gamma_lum, "GAMMA").text = "1.2"
        
        # RENDERFILE
        renderfile = ET.SubElement(lightsetup, "RENDERFILE")
        renderfile.text = f"render-{props.base_name[:-1]}.jpg"
        
        # Formater le XML avec indentation
        rough_string = ET.tostring(lightsetup, 'unicode')
        reparsed = minidom.parseString(rough_string)
        pretty_xml = reparsed.toprettyxml(indent="\t")
        
        # Sauvegarder le fichier XML dans le même dossier que les images
        xml_filename = f"colorstudio_{props.base_name[:-1]}.xml"
        xml_filepath = os.path.join(output_path, xml_filename)
        
        with open(xml_filepath, 'w', encoding='utf-8') as f:
            f.write(pretty_xml)
        
        return xml_filepath


class COLORSTUDIO_PT_panel(bpy.types.Panel):
    """Panel pour l'export Color Studio"""
    bl_label = "Color Studio Exporter"
    bl_idname = "COLORSTUDIO_PT_panel"
    bl_space_type = 'VIEW_3D'
    bl_region_type = 'UI'
    bl_category = "Color Studio"
    
    def draw(self, context):
        layout = self.layout
        props = context.scene.colorstudio_props
        
        # Section des paramètres
        box = layout.box()
        box.label(text="Export Settings:")
        
        box.prop(props, "output_directory")
        box.prop(props, "base_name")
        box.prop(props, "image_count")
        box.prop(props, "image_format")
        
        # Section résolution
        box = layout.box()
        box.label(text="Resolution:")
        row = box.row()
        row.prop(props, "resolution_x")
        row.prop(props, "resolution_y")
        
        # Rendu
        if context.scene.render.engine == 'CYCLES':
            box.prop(props, "render_samples")
        
        # Bouton d'export
        layout.operator("colorstudio.export_lights")


# Classes à enregistrer
classes = (
    ColorStudioExportProperties,
    COLORSTUDIO_OT_export_lights,
    COLORSTUDIO_PT_panel,
)

def register():
    """Enregistrer les classes et les propriétés"""
    for cls in classes:
        bpy.utils.register_class(cls)
    
    # Enregistrer les propriétés de la scène
    bpy.types.Scene.colorstudio_props = bpy.props.PointerProperty(
        type=ColorStudioExportProperties
    )

def unregister():
    """Désenregistrer les classes et les propriétés"""
    for cls in reversed(classes):
        bpy.utils.unregister_class(cls)
    
    del bpy.types.Scene.colorstudio_props

if __name__ == "__main__":
    register()