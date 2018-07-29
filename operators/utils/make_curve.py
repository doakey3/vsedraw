import bpy


def make_curve(scene, verts, name):
    """
    Make a 2D curve object with the given vertices

    Parameters
    ----------
    verts: list of lists of int
        The [[x, y]...] coordinates of the curve

    Returns
    -------
    3D object (the curve)
    """
    curve = bpy.data.curves.new(name, type='CURVE')
    #curve.dimensions = '3D'
    spline = curve.splines.new('POLY')
    spline.points.add(len(verts) - 1)

    for i in range(len(verts)):
        spline.points[i].co.x = verts[i][0]
        spline.points[i].co.y = verts[i][1]
        spline.points[i].co.z = 0

    obj = bpy.data.objects.new(name, curve)
    scene.objects.link(obj)

    for i in reversed(range(20)):
        obj.layers[i] = (i == 10)

    return obj
