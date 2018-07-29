import bpy
import os

folder_path = '/home/doakey/Desktop/letters'

def view_3d_context():
    for oWindow in bpy.context.window_manager.windows:
        oScreen = oWindow.screen
        for oArea in oScreen.areas:
            if oArea.type == 'VIEW_3D':
                for oRegion in oArea.regions:
                    if oRegion.type == 'WINDOW':
                        oContextOverride = {
                            'window': oWindow, 
                            'screen': oScreen, 
                            'area': oArea, 
                            'region': oRegion, 
                            'scene': bpy.context.scene, 
                            'edit_object': bpy.context.edit_object, 
                            'active_object': bpy.context.active_object, 
                            'selected_objects': bpy.context.selected_objects
                        }
                        return oContextOverride

def collect_ids():
    """
    Create a dictionary of object id's and their associated objects
    """
    id_dict = {}
    
    objs = sorted(bpy.context.scene.objects, key=lambda x: x.name)
    
    for obj in objs:
        if '_.' in obj.name and obj.type == 'CURVE':
            id = obj.name.split('_.')[0]
            if not id in id_dict.keys():
                id_dict[id] = [obj]
            else:
                id_dict[id].append(obj)
    return id_dict

def main():
    bpy.ops.object.select_all(action='DESELECT')
    ids = collect_ids()
    keys = list(ids.keys())
    context = view_3d_context()
    for key in keys:
        curves = ids[key]
        for curve in curves:
            curve.select = True
        
        if key == "\\" or key == "/":
            key = key + key
        path = os.path.join(folder_path, key + '.glyph')
        bpy.ops.tutorial_tools.export_glyph(filepath=path, correct_x=True)
        bpy.ops.object.select_all(action='DESELECT')
 
main()

    