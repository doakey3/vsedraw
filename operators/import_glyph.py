import bpy
import os
from bpy_extras.io_utils import ImportHelper

from .utils import make_glyph_strip

def view_3d_context():
    for oWindow in bpy.context.window_manager.windows:
        oScreen = oWindow.screen
        for oArea in oScreen.areas:
            if oArea.type == 'VIEW_3D':
                for oRegion in oArea.regions:
                    if oRegion.type == 'WINDOW':
                        oContextOverride = {
                            'window': oWindow,
                            'screen': oScreen,
                            'area': oArea,
                            'region': oRegion,
                            'scene': bpy.context.scene,
                            'edit_object': bpy.context.edit_object,
                            'active_object': bpy.context.active_object,
                            'selected_objects': bpy.context.selected_objects
                        }
                        return oContextOverride

def make_mesh(scene, verts, edges, faces, name="MyObj"):
    """
    Create a mesh object with the given vertices, edges, and faces & name
    """

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    scene.objects.link(obj)

    mesh.from_pydata(verts, edges, faces)

    mesh.update()
    return obj


class ImportGlyph(bpy.types.Operator, ImportHelper):
    bl_label = "Import Glyph"
    bl_idname = "vsedraw.import_glyph"
    bl_description = "Import a glyph and add a stroke to it"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob = bpy.props.StringProperty(
        default="*.glyph",
        options={"HIDDEN"},
        maxlen=255,
        )

    def execute(self, context):
        scene = context.scene
        scale = scene.vsedraw.scale

        fname = os.path.splitext(os.path.basename(self.filepath))[0]
        new_scene = bpy.data.scenes.new(fname)
        new_scene.render.fps = scene.render.fps
        new_scene.render.fps_base = scene.render.fps_base

        context.screen.scene= new_scene

        with open(self.filepath, 'r') as f:
            text = f.read().strip()

        lines = text.split('\n')

        curve_verts = []
        for line in lines:
            curve_verts.append(eval(line))

        all_x = []
        all_y = []
        for group in curve_verts:
            for vert in group:
                all_x.append(vert[0])
                all_y.append(vert[1])
        min_x = min(all_x)
        min_y = min(all_y)

        strip = make_glyph_strip(scene, new_scene, curve_verts)

        strip.transform.offset_x += min_x * 100 * scale
        strip.transform.offset_y = min_y * 100 * scale

        return {"FINISHED"}
