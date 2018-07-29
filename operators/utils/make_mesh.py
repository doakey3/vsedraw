import bpy


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
