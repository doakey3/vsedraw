import bpy
import bpy.utils.previews
import os
from .operators.utils.png import from_array

from .operators import ChangeColor
from .operators import ToggleGuide
from .operators import ExportGlyph
from .operators import Write
from .operators import ImportGlyph
from .operators import ImportStrokes
from .operators import Trace

bl_info = {
    "name": "VSE Draw",
    "description": "Reconstruct a drawing from the position of each stroke",
    "author": "doakey3",
    "version": (1, 0, 0),
    "blender": (2, 7, 9),
    "category": "Sequencer"}

icon_collections = {}
icons_loaded = False

def load_icons():
    global icon_collections
    global icons_loaded

    if icons_loaded: return icon_collections["main"]

    addon_icons = bpy.utils.previews.new()

    icons_dir = os.path.join(os.path.dirname(__file__), "icons")

    addon_icons.load('color_box_01', os.path.join(icons_dir, '01.png'), 'IMAGE')
    addon_icons.load('color_box_02', os.path.join(icons_dir, '02.png'), 'IMAGE')
    addon_icons.load('color_box_03', os.path.join(icons_dir, '03.png'), 'IMAGE')

    icon_collections["main"] = addon_icons
    icons_loaded = True

    return icon_collections["main"]

def clear_icons():
	global icons_loaded
	for icon in icon_collections.values():
		bpy.utils.previews.remove(icon)
	icon_collections.clear()
	icons_loaded = False


class SaveColor(bpy.types.Operator):
    bl_label = "Save Color"
    bl_idname = "vsedraw.save_color"
    bl_description = "Save selected color as fast pick color"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        global icons_loaded

        scene = context.scene

        red = int(scene.vsedraw.color_picker[0] * 255)
        green = int(scene.vsedraw.color_picker[1] * 255)
        blue = int(scene.vsedraw.color_picker[2] * 255)

        fname = scene.vsedraw.save_overs
        path = os.path.join(os.path.dirname(__file__), 'icons', fname)

        color_array = []
        for r in range(0, 32):
            color_array.append([])
            for c in range(0, 32):
                color_array[-1].append([red, green, blue])

        img = from_array(color_array, 'RGB')
        img.save(path)

        clear_icons()
        load_icons()

        return {"FINISHED"}


class VSEDrawProperties(bpy.types.PropertyGroup):
    color_picker = bpy.props.FloatVectorProperty(
       subtype='COLOR_GAMMA',
       description="Change Color of Stroke / Glyph",
       size=3,
       default=(0.75, 0.0, 0.0),
       min=0.0,
       max=1.0,
    )

    icons = load_icons()
    color_01 = icons.get('color_box_01')
    color_02 = icons.get('color_box_02')
    color_03 = icons.get('color_box_03')

    save_over_names = [
        ("01.png", "Color 1", "Save over Color 01"),
        ("02.png", "Color 2", "Save over Color 02"),
        ("03.png", "Color 3", "Save over Color 03"),
        ]

    save_overs = bpy.props.EnumProperty(
        name="Save Option",
        items=save_over_names,
        description="Save selected color over quick color",
        default="01.png"
    )

    scale = bpy.props.FloatProperty(
        name="Scale",
        description="Multiply the scale of imported glyphs",
        default=1.0,
        min=0.1
    )

    speed = bpy.props.FloatProperty(
        name="Speed",
        description="Pixels per second that the stroke will be drawn.",
        default=20.0,
        min=0.1,
    )

    thickness = bpy.props.IntProperty(
        name="Thickness",
        description="The thickness of the stroke in pixels.",
        default=10,
        min=1
    )

    decorator_types = [
        ("none", "None", ""),
        ("circle", "Circle", "Draw a circle the glyph"),
        ("box", "Box", "Draw a box around the glyph"),
        ("underline", "Underline", "Draw an underline under the glyph"),
        #("rounded_box", "Rounded Box", "Draw a rounded box around the glyph"),
        ("ellipse", "Ellipse", "Draw an ellipse around the glyph"),
        ]

    decorator = bpy.props.EnumProperty(
        name="Decorator",
        items=decorator_types,
        description="Set the decorator",
        default="none"
        )

    text = bpy.props.StringProperty()


class SeqUI(bpy.types.Panel):
    bl_space_type = "SEQUENCE_EDITOR"
    bl_region_type = "UI"
    bl_label = "Tutorial Tools"
    #bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Tools"

    @classmethod
    def poll(cls, context):
        return context.space_data.view_type == 'SEQUENCER'

    def draw(self, context):
        scene = context.scene

        icons = load_icons()
        color_01 = icons.get('color_box_01')
        color_02 = icons.get('color_box_02')
        color_03 = icons.get('color_box_03')

        layout = self.layout

        row = layout.row()
        row.operator("vsedraw.change_color", text="1", icon_value=color_01.icon_id).button="01.png"
        row.operator("vsedraw.change_color", text="2", icon_value=color_02.icon_id).button="02.png"
        row.operator("vsedraw.change_color", text="3", icon_value=color_03.icon_id).button="03.png"

        row = layout.row()
        row.prop(scene.vsedraw, "color_picker", text="")
        row.operator("vsedraw.change_color", text="", icon="FILE_REFRESH").button="None"
        row.prop(scene.vsedraw, "save_overs", text="")
        row.operator("vsedraw.save_color", text="", icon="DISK_DRIVE")

        row = layout.row()
        row.prop(scene.vsedraw, "scale")

        row = layout.row()
        row.prop(scene.vsedraw, "speed")

        row = layout.row()
        row.prop(scene.vsedraw, "thickness")

        row = layout.row()
        row.prop(scene.vsedraw, "decorator")

        row = layout.row()
        row.operator("vsedraw.write")
        row.prop(scene.vsedraw, "text", text="")

        row = layout.row()
        row.operator("vsedraw.import_glyph")

        row = layout.row()
        row.operator("vsedraw.import_strokes")

        row = layout.row()
        row.operator("vsedraw.trace")

class View3d_UI(bpy.types.Panel):
    bl_space_type = "VIEW_3D"
    bl_region_type = "TOOLS"
    bl_label = "Nurbs To Videos"
    #bl_options = {"DEFAULT_CLOSED"}
    bl_category = "Tools"

    def draw(self, context):
        scene = context.scene
        layout = self.layout

        row = layout.row()
        row.operator("vsedraw.export_glyph")

        row = layout.row()
        row.operator("vsedraw.toggle_guide")

def register():
    bpy.utils.register_module(__name__)

    bpy.types.Scene.vsedraw = bpy.props.PointerProperty(
        type=VSEDrawProperties)

def unregister():
    bpy.utils.unregister_module(__name__)

    clear_icons()

    del bpy.types.Scene.vsedraw.color_picker
    del bpy.types.Scene.vsedraw.save_overs
    del bpy.types.Scene.vsedraw.scale
    del bpy.types.Scene.vsedraw.speed
    del bpy.types.Scene.vsedraw.thickness
    del bpy.types.Scene.vsedraw.decorator

if __name__ == "__main__":
    register()
