import bpy
import math
from .make_mesh import make_mesh


def make_stroke_cap(radius, scene, origin_x=0, origin_y=0, start_angle=0, stop_angle=180, step_angle=5, offset_x=0, offset_y=0, name="Circle", color="#000000", layer=10):
    """
    Create a part of a circle object.

    Parameters
    ----------
    radius: float
    origin_x: float
        The x origin of the circle
    origin_y: float
        The y origin of the circle
    start_angle: float
        The start_angle in degrees
    stop_angle: float
        The stop_angle in degrees
    step_angle: float
        The amount to turn for each vertex on the circumference
    offset_x: float
        The x offset of the object
    offset_y: float
        The y offset of the object
    name: str
    color: str
    layer: int
        The layer where the object will go (1-20)

    Returns
    -------
    The circle object
    """
    verts = []

    count = abs(int(start_angle - stop_angle / step_angle))

    for i in range(count + 1):
        angle = (step_angle * i) + start_angle

        x = math.sin(math.radians(angle)) * radius
        x = x + origin_x + offset_x

        y = math.cos(math.radians(angle)) * radius
        y = y + origin_y + offset_y

        verts.append([x, y, 0])

    edges = []
    for i in range(len(verts) - 1):
        edges.append((i, i + 1))
    edges.append((0, len(verts) - 1))

    faces = []
    for i in range(len(verts)):
        faces.append(i)

    faces = [faces]

    if angle < 0:
        obj = make_mesh(scene, verts, edges, faces, name)
    else:
        obj = make_mesh(scene, list(reversed(verts)), edges, faces, name)

    # Due to Blender bug, the following code does not work
    # Will update in future
    #for i in reversed(range(20)):
    #    obj.layers[i] = (i == layer)

    # Here is a workaround

    obj.location[0] = -100000

    return obj
