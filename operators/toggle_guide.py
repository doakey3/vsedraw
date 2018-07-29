import bpy

def make_mesh(verts, edges, faces, name):
    scene = bpy.context.scene

    mesh = bpy.data.meshes.new(name)
    obj = bpy.data.objects.new(name, mesh)
    bpy.context.scene.objects.link(obj)

    mesh.from_pydata(verts, edges, faces)
    mesh.update()


class ToggleGuide(bpy.types.Operator):
    bl_label = "Toggle Guide"
    bl_idname = "vsedraw.toggle_guide"
    bl_description = "Create a box to guide how to make drawings for 1080p"
    bl_options = {'REGISTER', 'UNDO'}


    def execute(self, context):
        scene = context.scene

        guide_found = False
        for obj in scene.objects:
            if obj.name == "draw_guide":
                guide_found = True

        if not guide_found:
            verts = [(0.0, 0.0, 0.0), (0.0, 10.8, 0.0), (19.2, 10.8, 0.0), (19.2, 0.0, 0.0)]
            edges = [(0, 1), (1, 2), (2, 3), (0, 3)]
            faces = []
            make_mesh(verts, edges, faces, 'draw_guide')

        else:
            selected = context.selected_objects

            guide = scene.objects['draw_guide']
            bpy.ops.object.select_all(action='DESELECT')
            guide.select = True
            bpy.ops.object.delete()

            for obj in selected:
                obj.select = True

        return {"FINISHED"}
