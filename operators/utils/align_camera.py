import bpy


def align_camera(scene, x_max, y_max, x_min, y_min, thickness, scale):
    """
    Aligns camera so that only the glyph is in view and sets render mode
    to alpha background

    Parameters
    ----------
    glyph_width: float
    glyph_height: float
    thickness: int
        The thickness of the stroke
    """
    camera = scene.camera

    if not camera:
        cam = bpy.data.cameras.new("Camera")
        camera = bpy.data.objects.new("Camera", cam)
        scene.objects.link(camera)
        scene.camera = camera

    glyph_width = x_max - x_min
    glyph_height = y_max - y_min

    camera.location[0] = x_min + (glyph_width / 2)
    camera.location[1] = y_min + (glyph_height / 2)
    camera.location[2] = 1

    camera.rotation_euler[0] = 0
    camera.rotation_euler[1] = 0
    camera.rotation_euler[2] = 0

    width = glyph_width + thickness
    height = glyph_height + thickness

    ortho_scale = max(width, height)

    camera.data.type = "ORTHO"
    camera.data.ortho_scale = ortho_scale

    scene.render.resolution_x = width * 100
    scene.render.resolution_y = height * 100
    scene.render.resolution_percentage = 100
    scene.render.alpha_mode = "TRANSPARENT"
