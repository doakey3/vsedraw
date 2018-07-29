import bpy
from .utils.png import Reader
import os


def get_color(filepath):
    reader = Reader(filepath)
    map_obj = reader.asDirect()[2]
    color = []
    for row in map_obj:
        x = list(row)
        color = [x[0] / 255, x[1] / 255, x[2] / 255]
        break
    return color


class ChangeColor(bpy.types.Operator):
    bl_label = "Change Color"
    bl_idname = "vsedraw.change_color"
    bl_description = "Change color of selected strips"
    bl_options = {'REGISTER', 'UNDO'}

    button = bpy.props.StringProperty(
        name="Button",
        default="None"
    )

    @classmethod
    def poll(self, context):
        scene = context.scene
        if (scene and scene.sequence_editor):
            return True
        else:
            return False

    def execute(self, context):
        scene = context.scene

        if not self.button == "None":
            button_path = os.path.join(os.path.dirname(__file__), '..', 'icons', self.button)
            color = get_color(button_path)
        else:
            r = scene.vsedraw.color_picker[0]
            g = scene.vsedraw.color_picker[1]
            b = scene.vsedraw.color_picker[2]
            color = [r, g, b]

        strips = context.selected_sequences

        all_strips = sorted(scene.sequence_editor.sequences, key=lambda x: x.frame_final_end)

        current_frame = scene.frame_current
        empty_frame = all_strips[-1].frame_final_end + 1

        scene.frame_current = empty_frame

        for strip in strips:
            curve = None
            for modifier in strip.modifiers:
                if modifier.type == "CURVES":
                    if modifier.name == "invert":
                        curve = modifier
                        break

            if not curve:
                scene.sequence_editor.active_strip = strip
                bpy.ops.sequencer.strip_modifier_add(type='CURVES')
                modifier = strip.modifiers[-1]
                modifier.name = "invert"
                curve = modifier

            red, green, blue, combo = curve.curve_mapping.curves
            combo.points[0].location[1] = 1
            combo.points[1].location[1] = 0


        for strip in strips:
            scene.sequence_editor.active_strip = strip
            for modifier in strip.modifiers:
                if modifier.type == "CURVES":
                    if modifier.name == "color":
                        bpy.ops.sequencer.strip_modifier_remove(name="color")
                        break

            bpy.ops.sequencer.strip_modifier_add(type="CURVES")
            modifier = strip.modifiers[-1]
            modifier.name = "color"
            curve = modifier

            red, green, blue, combo = curve.curve_mapping.curves
            red.points[1].location[1] = color[0]
            green.points[1].location[1] = color[1]
            blue.points[1].location[1] = color[2]

            curve.curve_mapping.update()

        scene.frame_current = current_frame
        return {"FINISHED"}
