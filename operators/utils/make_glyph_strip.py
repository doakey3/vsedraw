import bpy
import copy
import math
import numpy as np

from .make_stroke_cap import make_stroke_cap
from .make_curve import make_curve
from .make_stroke import make_stroke
from .align_camera import align_camera
from .get_curve_length import get_curve_length
from .distance_formula import distance_formula


def ellipse(t, a, b):
    return [a * math.cos(t), b * math.sin(t)]

def ellipse_points(origin_x, origin_y, a, b):
    """
    Return the points that make up an ellipse with radii of a & b
    """
    points = []
    for t in np.linspace(0, 2 * math.pi, 100):
        points.append(ellipse(t, a, b))
    for point in points:
        point[0] += origin_x
        point[1] += origin_y
    return points


def make_glyph_strip(old_scene, new_scene, curve_verts, channel=1):
    scale = old_scene.vsedraw.scale
    thickness = old_scene.vsedraw.thickness / 100
    speed = old_scene.vsedraw.speed / 100

    width = 0.001

    make_stroke_cap(radius=thickness / 2, scene=new_scene,
                    offset_x=-width, step_angle=5, name=new_scene.name + "_stroke_head")
    make_stroke_cap(radius=thickness / 2, scene=new_scene,
                    offset_x=width, step_angle=-5, name=new_scene.name + "_stroke_tail")

    count = len(str(len(curve_verts) + 1))

    all_verts = []
    current_frame = 1

    for i in range(len(curve_verts)):
        if i > 0:
            x1 = curve_verts[i - 1][-1][0] * scale
            y1 = curve_verts[i - 1][-1][1] * scale

            x2 = curve_verts[i][0][0] * scale
            y2 = curve_verts[i][0][1] * scale

            p1 = [x1, y1]
            p2 = [x2, y2]

            distance = distance_formula(p1, p2)
            extra_frames = int(distance / speed)
            current_frame += extra_frames

        verts = copy.deepcopy(curve_verts[i])

        for vert in verts:
            vert[0] *= scale
            vert[1] *= scale

            if old_scene.vsedraw.decorator == "underline":
                vert[0] += thickness
            elif old_scene.vsedraw.decorator == "box":
                vert[0] += thickness * 2
                vert[1] += thickness * 2

        name = new_scene.name + '_' + str(i).zfill(count)

        curve = make_curve(new_scene, verts, name)

        length = get_curve_length(curve)
        frames = int(length / speed)

        make_stroke(new_scene, thickness, width, curve, current_frame - 1, current_frame + frames)
        current_frame += frames

        all_verts.extend(verts)

    x_max = max(all_verts, key=lambda v: v[0])[0]
    x_min = min(all_verts, key=lambda v: v[0])[0]
    y_max = max(all_verts, key=lambda v: v[1])[1]
    y_min = min(all_verts, key=lambda v: v[1])[1]

    if not old_scene.vsedraw.decorator == "none":
        if old_scene.vsedraw.decorator == "underline":
            new_verts = [[0, thickness * 0.75], [x_max + thickness, thickness * 0.75]]
        elif old_scene.vsedraw.decorator == "box":
            new_verts = [
                [0, y_max + thickness * 2],
                [thickness, y_max + thickness * 2],
                [x_max + thickness, y_max + thickness * 2],
                [x_max + thickness * 2, y_max + thickness * 2],
                [x_max + thickness * 2, y_max + thickness],
                [x_max + thickness * 2, y_min - thickness],
                [x_max + thickness * 2, y_min - thickness * 2],
                [x_max + thickness, y_min - thickness * 2],
                [thickness, y_min - thickness * 2],
                [0, y_min - thickness * 2],
                [0, y_min + thickness],
                [0, y_max + thickness * 2]
            ]
        elif old_scene.vsedraw.decorator == "circle":
            origin_x = ((x_max - x_min) / 2) + x_min
            origin_y = ((y_max - y_min) / 2) + y_min
            radius = (max([x_max - x_min, y_max - y_min]) / 2) + thickness * 2
            new_verts = ellipse_points(origin_x, origin_y, radius, radius)

        elif old_scene.vsedraw.decorator == "ellipse":
            origin_x = ((x_max - x_min) / 2) + x_min
            origin_y = ((y_max - y_min) / 2) + y_min
            a = ((x_max - x_min) / 2) + thickness * 4
            b = ((y_max - y_min) / 2) + thickness * 4
            new_verts = ellipse_points(origin_x, origin_y, a, b)

        x1 = all_verts[-1][0]
        y1 = all_verts[-1][1]

        x2 = new_verts[0][0]
        y2 = new_verts[0][1]

        p1 = [x1, y1]
        p2 = [x2, y2]

        distance = distance_formula(p1, p2)
        extra_frames = int(distance / speed)
        current_frame += extra_frames

        all_verts.extend(new_verts)
        curve = make_curve(new_scene, new_verts, "decorator")
        length = get_curve_length(curve)
        frames = int(length / speed)

        make_stroke(new_scene, thickness, width, curve, current_frame - 1, current_frame + frames)
        current_frame += frames

        x_max = max(all_verts, key=lambda v: v[0])[0]
        x_min = min(all_verts, key=lambda v: v[0])[0]
        y_max = max(all_verts, key=lambda v: v[1])[1]
        y_min = min(all_verts, key=lambda v: v[1])[1]

    align_camera(new_scene, x_max, y_max, x_min, y_min, thickness, scale)
    new_scene.frame_end = current_frame + 1

    bpy.ops.wm.context_set_string(data_path="area.type", value="VIEW_3D")
    bpy.ops.render.render()

    bpy.context.screen.scene = old_scene
    bpy.ops.wm.context_set_string(data_path="area.type", value="SEQUENCE_EDITOR")

    bpy.ops.sequencer.scene_strip_add(frame_start=old_scene.frame_current, channel=1, scene=new_scene.name)

    strip = old_scene.sequence_editor.active_strip

    bpy.ops.sequencer.strip_modifier_add(type='CURVES')
    curve = strip.modifiers[-1]
    curve.name = "white"
    red, green, blue, combo = curve.curve_mapping.curves
    combo.points[0].location[1] = 1
    combo.points[1].location[1] = 1

    strip.use_translation = True

    res_x = old_scene.render.resolution_x
    res_y = old_scene.render.resolution_y

    #bpy.ops.sequencer.meta_make()

    #metastrip = old_scene.sequence_editor.active_strip

    strip.blend_type = "ALPHA_OVER"
    strip.use_translation = True

    #metastrip.use_crop = True
    #metastrip.crop.max_x = res_x - ((x_max + thickness) * 100)
    #metastrip.crop.max_y = res_y - (y_max * 100)

    strip.channel = channel
    #metastrip.name = 'META-' + strip.name

    return strip

