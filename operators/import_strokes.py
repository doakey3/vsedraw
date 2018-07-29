import bpy
from bpy_extras.io_utils import ImportHelper

import os
import copy

from .utils import make_glyph_strip
from .utils import distance_formula
from .utils import get_open_channel
from .utils import get_fit_channel

class ImportStrokes(bpy.types.Operator, ImportHelper):
    bl_label = "Import Strokes"
    bl_idname = "vsedraw.import_strokes"
    bl_description = "Import a glyph's strokes as separate strips"
    bl_options = {'REGISTER', 'UNDO'}

    filter_glob = bpy.props.StringProperty(
        default="*.glyph",
        options={"HIDDEN"},
        maxlen=255,
        )

    def execute(self, context):
        scene = context.scene

        first_frame = scene.frame_current

        fname = os.path.splitext(os.path.basename(self.filepath))[0]

        added_strips = []

        scale = scene.vsedraw.scale
        speed = scene.vsedraw.speed / 100

        with open(self.filepath, 'r') as f:
            text = f.read().strip()

        lines = text.split('\n')

        curve_verts = []
        for line in lines:
            curve_verts.append(eval(line))

        new_verts = copy.deepcopy(curve_verts)
        for i in range(len(curve_verts)):
            min_x = float(min(curve_verts[i], key=lambda v: v[0])[0])
            min_y = float(min(curve_verts[i], key=lambda v: v[1])[1])

            if i > 0:
                x1 = curve_verts[i - 1][-1][0] * scale
                y1 = curve_verts[i - 1][-1][1] * scale

                x2 = curve_verts[i][0][0] * scale
                y2 = curve_verts[i][0][1] * scale

                p1 = [x1, y1]
                p2 = [x2, y2]

                distance = distance_formula(p1, p2)
                extra_frames = distance / speed
                scene.frame_current += extra_frames

            for vert in new_verts[i]:
                vert[0] -= min_x
                vert[1] -= min_y

            fname = os.path.splitext(os.path.basename(self.filepath))[0]
            new_scene = bpy.data.scenes.new(fname)
            new_scene.render.fps = scene.render.fps
            new_scene.render.fps_base = scene.render.fps_base
            context.screen.scene= new_scene

            open_channel = get_open_channel(scene)

            strip = make_glyph_strip(scene, new_scene, [new_verts[i]], channel=open_channel)

            strip.transform.offset_x = min_x * 100 * scale
            strip.transform.offset_y = min_y * 100 * scale

            added_strips.append(strip)

            scene.frame_current = strip.frame_final_end

        for strip in added_strips:
            strip.frame_final_end = added_strips[-1].frame_final_end
            strip.channel = get_fit_channel(scene, strip)

        scene.frame_current = first_frame

        return {"FINISHED"}
