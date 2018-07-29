import bpy
import math


def distance_formula(p1, p2):
    """
    Calculate the distance between 2 points on a 2D Cartesian coordinate plane
    """
    x = p2[0] - p1[0]
    y = p2[1] - p1[1]

    distance = math.sqrt(x**2 + y**2)
    return distance


def get_stroke_endpoints(stroke_body, scene):
    width = 0.001

    curve = stroke_body.modifiers[-1].object
    v_points = curve.data.splines.active.points
    points = []
    for vp in v_points:
        points.append([vp.co.x, vp.co.y])

    fcurve = bpy.data.actions[stroke_body.name + 'Action'].fcurves[0]

    start_frame = fcurve.keyframe_points[0].co[0]
    end_frame = fcurve.keyframe_points[-1].co[0]
    count_step = (fcurve.keyframe_points[-1].co[1] - fcurve.keyframe_points[0].co[1]) / (end_frame - start_frame)

    step_distance = width * count_step
    remaining = step_distance

    endpoints = [points[0]]

    i = 1
    while i < len(points):
        p1 = points[i - 1]
        p2 = points[i]

        distance = distance_formula(p1, p2)
        x = p2[0] - p1[0]
        y = p2[1] - p1[1]

        if distance < remaining:
            remaining -= distance
            i += 1

        else:
            step_x = (remaining / distance) * x
            step_y = (remaining / distance) * y

            e_point = [step_x + p1[0], step_y + p1[1]]
            endpoints.append(e_point)
            points[i - 1] = e_point
            remaining = step_distance

    endpoints.append(points[-1])

    return start_frame, endpoints


def get_glyph_points(stroke_bodies, scene):
    data = []
    for stroke_body in stroke_bodies:
        data.append(get_stroke_endpoints(stroke_body, scene))

    return data


def get_strip_box(strip):
    """
    Gets the box of a non-transform strip

    Args
        :strip: A strip from the vse (bpy.types.Sequence)
    Returns
        :box: A list comprising the strip's left, right, bottom, top
              (list of int)
    """
    scene = bpy.context.scene

    res_x = scene.render.resolution_x
    res_y = scene.render.resolution_y

    proxy_facs = {
        'NONE': 1.0,
        'SCENE': 1.0,
        'FULL': 1.0,
        'PROXY_100': 1.0,
        'PROXY_75': 0.75,
        'PROXY_50': 0.5,
        'PROXY_25': 0.25
    }

    proxy_key = bpy.context.space_data.proxy_render_size
    proxy_fac = proxy_facs[proxy_key]

    if not strip.use_translation and not strip.use_crop:
        left = 0
        right = res_x
        bottom = 0
        top = res_y

    elif strip.use_crop and not strip.use_translation:
        left = 0
        right = res_x
        bottom = 0
        top = res_y

    elif not hasattr(strip, 'elements'):
        len_crop_x = res_x
        len_crop_y = res_y

        if strip.type == "SCENE":
            len_crop_x = strip.scene.render.resolution_x
            len_crop_y = strip.scene.render.resolution_y
        if strip.use_crop:
            len_crop_x -= (strip.crop.min_x + strip.crop.max_x)
            len_crop_y -= (strip.crop.min_y + strip.crop.max_y)

            if len_crop_x < 0:
                len_crop_x = 0
            if len_crop_y < 0:
                len_crop_y = 0

        left = 0
        right = res_x
        bottom = 0
        top = res_y

        if strip.use_translation:
            left = strip.transform.offset_x
            right = left + len_crop_x
            bottom = strip.transform.offset_y
            top = strip.transform.offset_y + len_crop_y

    elif strip.use_translation and not strip.use_crop:
        left = strip.transform.offset_x
        right = left + (strip.elements[0].orig_width / proxy_fac)
        bottom = strip.transform.offset_y
        top = bottom + (strip.elements[0].orig_height / proxy_fac)

    else:
        total_crop_x = strip.crop.min_x + strip.crop.max_x
        total_crop_y = strip.crop.min_y + strip.crop.max_y

        len_crop_x = (strip.elements[0].orig_width / proxy_fac) - total_crop_x
        len_crop_y = (strip.elements[0].orig_height / proxy_fac) - total_crop_y

        left = strip.transform.offset_x
        right = left + len_crop_x
        bottom = strip.transform.offset_y
        top = bottom + len_crop_y

    box = [left, right, bottom, top]

    return box


class Trace(bpy.types.Operator):
    bl_label = "Trace"
    bl_idname = "vsedraw.trace"
    bl_description = "Trace active strip to selected"
    bl_options = {'REGISTER', 'UNDO'}

    def execute(self, context):
        scene = context.scene
        scale = scene.vsedraw.scale
        thickness = scene.vsedraw.thickness

        active = scene.sequence_editor.active_strip
        if not active.use_translation:
            active.use_translation = True

        left, right, bottom, top = get_strip_box(active)
        active_width = right - left
        active_height = top - bottom

        selected = []
        for strip in sorted(context.selected_sequences, key=lambda s: s.name):
            if not strip == active and strip.type == "SCENE":
                selected.append(strip)

        for strip in selected:
            stroke_bodies = []
            for obj in sorted(strip.scene.objects, key=lambda o: o.name):
                if obj.type == "MESH" and not "_stroke_head" in obj.name and not "_stroke_tail" in obj.name:
                    stroke_bodies.append(obj)
                elif obj.type == "CAMERA":
                    camera = obj

            data = get_glyph_points(stroke_bodies, strip.scene)
            all_points = []
            for i in range(len(data)):
                all_points.extend(data[i][1])
            x_min = min(all_points, key=lambda v: v[0])[0]
            y_min = min(all_points, key=lambda v: v[1])[1]

            for i in range(len(data)):
                for p in range(len(data[i][1])):
                    data[i][1][p][0] *= 100
                    data[i][1][p][0] += strip.transform.offset_x
                    data[i][1][p][0] -= x_min * 100
                    data[i][1][p][0] -= active_width / 2
                    data[i][1][p][0] += thickness / 2

                    data[i][1][p][1] *= 100
                    data[i][1][p][1] += strip.transform.offset_y
                    data[i][1][p][1] -= y_min * 100
                    data[i][1][p][1] -= active_height / 2
                    data[i][1][p][1] += thickness / 2

                    active.transform.offset_x = data[i][1][p][0]
                    active.transform.offset_y = data[i][1][p][1]

                    active.transform.keyframe_insert(data_path="offset_x", frame=strip.frame_final_start + data[i][0] + p - 1)
                    active.transform.keyframe_insert(data_path="offset_y", frame=strip.frame_final_start + data[i][0] + p - 1)


        return {"FINISHED"}
