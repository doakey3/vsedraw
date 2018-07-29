import bpy
from .make_mesh import make_mesh
from .get_curve_length import get_curve_length

def make_stroke(scene, thickness, width, curve, start_frame, end_frame):
    """
    Draw a stroke
    """
    verts = [
        (0.0, thickness / 2, 0),
        (width, thickness / 2, 0),
        (width, -thickness / 2, 0),
        (0, -thickness / 2, 0)
    ]

    edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
    faces = [(3, 2, 1, 0)]
    obj = make_mesh(scene, verts, edges, faces, scene.name + '_stroke-body')

    modifier = obj.modifiers.new("array", "ARRAY")
    modifier.start_cap = scene.objects[scene.name + '_stroke_tail']
    modifier.end_cap = scene.objects[scene.name + '_stroke_head']
    modifier.count = 1
    modifier.keyframe_insert(data_path="count", frame=start_frame)

    obj.hide = True
    obj.hide_render = True
    obj.keyframe_insert(data_path="hide", frame=start_frame)
    obj.keyframe_insert(data_path="hide_render", frame=start_frame)

    obj.hide = False
    obj.hide_render = False
    obj.keyframe_insert(data_path="hide", frame=start_frame + 1)
    obj.keyframe_insert(data_path="hide_render", frame=start_frame + 1)

    curve_length = get_curve_length(curve)
    modifier.count += int(curve_length / 0.001)
    modifier.keyframe_insert(data_path="count", frame=end_frame)

    modifier = obj.modifiers.new("curve", "CURVE")
    modifier.object = curve
