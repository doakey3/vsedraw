import bpy
from .hex2rgb import hex2rgb


def add_material(obj, color):
    """
    Set the first material of an object to the given color and make it
    shadeless


    Parameters
    ----------
    color: str
        The color to use for the material as a hexcode, ie: #456B73
    """

    try:
        material = bpy.data.materials["stroke"]
    except KeyError:
        material = bpy.data.materials.new(name="stroke")

    #color = hex2rgb(color)

    material.diffuse_color = (1, 1, 1)
    material.use_shadeless = True

    """
    material.use_nodes = True

    node_tree = material.node_tree
    #node_tree.nodes.remove(node_tree.nodes[1])

    emission = node_tree.nodes.new("ShaderNodeEmission")
    emission.inputs[0].default_value = (1, 1, 1, 1)
    material.diffuse_color = (1, 1, 1)

    output = node_tree.nodes[0]

    links = node_tree.links
    links.new(emission.outputs[0], output.inputs[0])

    """

    obj.data.materials.append(material)
