import bpy
from bpy_extras.io_utils import ExportHelper


def convert_curve(obj):
    """
    Duplicate a curve and convert the duplicate to a mesh
    """
    bpy.ops.object.select_all(action='DESELECT')
    bpy.context.scene.objects.active = obj
    obj.select = True
    bpy.ops.object.duplicate()

    bpy.ops.object.convert(target='MESH')


def delete_visible_meshes():
    """
    Delete VISIBLE objects that are not curves
    """
    bpy.ops.object.select_all(action='DESELECT')
    objs = bpy.context.scene.objects
    for obj in objs:
        if obj.type == "MESH" and not obj.hide:
            obj.select = True

    bpy.ops.object.delete(use_global=False)


def hide_meshes():
    """
    Hide all mesh objects
    """
    objs = bpy.context.scene.objects
    for obj in objs:
        if obj.type == "MESH":
            obj.hide = True


def unhide_meshes():
    """
    Unhide all mesh objects
    """
    objs = bpy.context.scene.objects
    for obj in objs:
        if obj.type == "MESH":
            obj.hide = False


def get_group_size(meshes):
    """
    Get the box that includes all curves
    """
    x_coords = []
    y_coords = []
    for obj in meshes:
        mesh = obj.data
        for vertex in mesh.vertices:
            x_coords.append(vertex.co.x)
            y_coords.append(vertex.co.y)

    return min(x_coords), min(y_coords), max(x_coords), max(y_coords)


class ExportGlyph(bpy.types.Operator, ExportHelper):
    bl_label = "Export Glyph"
    bl_idname = "vsedraw.export_glyph"
    bl_description = "Export all curve point data into alphabetically as a glyph"
    bl_options = {'REGISTER', 'UNDO'}

    filename_ext = ".glyph"

    correct_x = bpy.props.BoolProperty(name="correct_x", default=False)
    correct_y = bpy.props.BoolProperty(name="correct_y", default=False)

    @classmethod
    def poll(cls, context):
        for obj in context.selected_objects:
            if obj.type == "CURVE":
                return True
        return False

    def execute(self, context):
        scene = context.scene
        output = []

        for area in context.screen.areas:
            if area.type == "VIEW_3D":
                used_layers = list(area.spaces[0].layers)
                area.spaces[0].layers[1] = True
                break

        for layer in scene.layers:
            layer = True

        hide_meshes()

        objs = sorted(context.selected_objects, key=lambda o: o.name)
        for obj in objs:
            if obj.type == "CURVE" and not obj.hide:
                convert_curve(obj)

        meshes = []
        for obj in context.scene.objects:
            if obj.type == "MESH" and not obj.hide:
                meshes.append(obj)

        min_x, min_y, max_x, max_y = get_group_size(meshes)

        for obj in sorted(meshes, key=lambda m: m.name):
            verts = []

            scene.objects.active = obj
            bpy.ops.object.mode_set(mode='EDIT')
            bpy.ops.mesh.select_all(action='SELECT')
            bpy.ops.mesh.dissolve_limited()
            bpy.ops.object.mode_set(mode='OBJECT')

            for vertex in obj.data.vertices:
                if self.correct_x and self.correct_y:
                    verts.append([round(vertex.co.x - min_x, 5), round(vertex.co.y - min_y, 5)])
                elif self.correct_x and not self.correct_y:
                    verts.append([round(vertex.co.x - min_x, 5), round(vertex.co.y, 5)])
                elif not self.correct_x and self.correct_y:
                    verts.append([round(vertex.co.x, 5), round(vertex.co.y - min_y, 5)])
                else:
                    verts.append([round(vertex.co.x, 5), round(vertex.co.y, 5)])
                verts.append([round(vertex.co.x, 5), round(vertex.co.y, 5)])

            output.append(str(verts))

        with open(self.filepath, 'w') as f:
            f.write('\n'.join(output))

        delete_visible_meshes()

        for i in range(len(used_layers)):
            scene.layers[i] = used_layers[i]

        return {"FINISHED"}
